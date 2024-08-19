import re
import traceback
from typing import Iterator
import faiss
import numpy as np
from bs4 import BeautifulSoup
import llamafile_client as llamafile
import os
import requests
import json
import logging
import shutil
import settings
from pathlib import Path

logger = logging.getLogger(__name__)

class Llama:

    def __init__(self):
        logging.basicConfig(
            format="%(asctime)s - %(levelname)s - %(name)s -   %(message)s",
            datefmt="%m/%d/%Y %H:%M:%S",
            level=logging.INFO,
        )
        self.build_index()

    def chunk_text(self, text: str) -> Iterator[str]:
        if settings.INDEX_TEXT_CHUNK_LEN > 0:
            chunk_len = min(settings.INDEX_TEXT_CHUNK_LEN, settings.EMBEDDING_MODEL_MAX_LEN)
        else:
            chunk_len = settings.EMBEDDING_MODEL_MAX_LEN

        text = re.sub(r"\s+", " ", text)
        tokens = llamafile.tokenize(text, base_url_prefix=settings.EMBEDDING_MODEL_URL, port=settings.EMBEDDING_MODEL_PORT)
        for i in range(0, len(tokens), chunk_len):
            yield llamafile.detokenize(tokens[i : i + chunk_len], base_url_prefix=settings.EMBEDDING_MODEL_URL, port=settings.EMBEDDING_MODEL_PORT)


    def load_data_for_indexing(self) -> Iterator[str]:
        for url in settings.INDEX_URLS:
            try:
                print(f'load_data_for_indexing: {url}')
                response = requests.get(url)
                response.raise_for_status()
                text = BeautifulSoup(response.text, "html.parser").get_text()
                for chunk in self.chunk_text(text):
                    yield chunk
            except Exception as e:
                traceback.print_exc()
                logger.error(f"skipping {url}: {e}")
                continue

        for directory in settings.INDEX_LOCAL_DATA_DIRS:
            for path in Path(directory).rglob("*.txt"):
                print(f'load_data_for_indexing: {path}')
                with open(path, "r") as f:
                    text = f.read()
                    for chunk in self.chunk_text(text):
                        yield chunk
        print(f'load_data_for_indexing is done!')

    def load_data_for_tmp_indexing(self) -> Iterator[str]:
        for path in Path(settings.INDEX_TMP_DATA_DIR).rglob("*.txt"):
            print(f'load_data_for_tmp_indexing: {path}')
            with open(path, "r") as f:
                text = f.read()
                for chunk in self.chunk_text(text):
                    yield chunk

    def embed(self, text: str) -> np.ndarray:
        embedding = llamafile.embed(text, settings.EMBEDDING_MODEL_URL)
        faiss.normalize_L2(embedding)
        return embedding


    def build_index(self):
        saveDir = Path(settings.INDEX_SAVE_DIR)
        if saveDir.exists():
            logger.info("index already exists @ %s, will not overwrite", saveDir)
            return
        embedding_dim = llamafile.embed("Apples are red.", settings.EMBEDDING_MODEL_URL).shape[-1]
        index = faiss.IndexFlatIP(embedding_dim)
        docs = []
        for text in self.load_data_for_indexing():
            embedding = self.embed(text)
            index.add(embedding)
            docs.append(text)

        saveDir.mkdir(parents=True)
        faiss.write_index(index, str(saveDir / "index.faiss"))
        with open(saveDir / "index.json", "w") as fout:
            json.dump(docs, fout)

    def append_index(self, index, docs):
        saveDir = Path(settings.INDEX_SAVE_DIR)
        for text in self.load_data_for_tmp_indexing():
            embedding = self.embed(text)
            index.add(embedding)
            docs.append(text)
        saveDir.mkdir(parents=True)
        faiss.write_index(index, str(saveDir / "index.faiss"))
        with open(saveDir / "index.json", "w") as fout:
            json.dump(docs, fout)

    def load_index(self):
        saveDir = Path(settings.INDEX_SAVE_DIR)
        if not saveDir.exists():
            raise FileNotFoundError(f"index not found @ {saveDir}")

        index = faiss.read_index(str(saveDir / "index.faiss"))
        logger.info("index with %d entries loaded from %s", index.ntotal, saveDir)

        with open(saveDir / "index.json", "r") as fin:
            docs = json.load(fin)
        return index, docs


    def pprint_search_results(self, scores: np.ndarray, doc_indices: np.ndarray, docs: list[str]):
        print("=== Search Results ===")
        for i, doc_ix in enumerate(doc_indices[0]):
            print('%.4f - "%s"' % (scores[0, i], docs[doc_ix][:100]))
        print()

    SEP = "-"*80

    def run_query(self, k: int, index: faiss.IndexFlatIP, query, docs: list[str]):
        emb = self.embed(query)
        scores, doc_indices = index.search(emb, k)
        search_results = [docs[ix] for ix in doc_indices[0]]
        prompt_template = (
            "You are an expert Q&A system. Answer the user's query using the provided context information.\n"
            "Context information:\n"
            "%s\n"
            "Query: %s"
        )
        prompt = prompt_template % ("\n".join(search_results), query)
        prompt_ntokens = len(llamafile.tokenize(prompt, base_url_prefix=settings.GENERATION_MODEL_URL, port=settings.GENERATION_MODEL_PORT))
        # print(f"(prompt_ntokens: {prompt_ntokens})")
        answer = llamafile.completion(prompt, base_url_prefix=settings.GENERATION_MODEL_URL)
        answer = answer.replace('what?\nAnswer: ', '').replace('</s>', '').strip()
        print(f'"{answer}"')
        return answer

    def rag(self, k_search_results: int):
        index, docs = self.load_index()
        while True:
            self.run_query(k_search_results, index, docs)

    def reload(self):
        if os.path.exists('./index-toy'):
            shutil.rmtree('./index-toy')
        self.build_index()
        return self.load_index()

    def reset(self):
        if os.path.exists(settings.INDEX_TMP_DATA_DIR):
            shutil.rmtree(settings.INDEX_TMP_DATA_DIR)
        if os.path.exists('./index-toy'):
            shutil.rmtree('./index-toy')
        Path(settings.INDEX_TMP_DATA_DIR).mkdir(parents=True)
        self.build_index()
        return self.load_index()

    def applyidx(self, source, target):
        if os.path.exists(target):
            os.remove(target)
        shutil.move(source, target)
        index, docs = self.load_index()
        if os.path.exists('./index-toy'):
            shutil.rmtree('./index-toy')
        self.append_index(index, docs)
        return self.load_index()
