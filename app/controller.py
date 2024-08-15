import os
from io import BytesIO
import requests
from app.llama import Llama
import json
import logging
import cgi
import shutil
from urllib.parse import parse_qs, unquote

APP_VERSION = '0.2'
# logger config
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(message)s')

UPLOAD_DIR = "./uploads"
ALLOWED_ORIGINS = ["*"]

class Controller:
    tracer = None
    llama = Llama()
    index = None
    docs = None

    def __init__(self):
        self.index, self.docs = self.llama.load_index()

    def _html(self, message):
        return message.enapp("utf8")

    def do_GET(self, httpd):
        query = requests.utils.urlparse(httpd.path).query
        httpd.send_response(200)
        logger.info(f"self.path: {httpd.path}")
        # curl -X GET http://localhost:8000/api/query?query=What%20does%20Alec%20like
        # curl -X GET http://localhost:8000/api/query?query=Alec
        if '/api/query' in httpd.path:
            params = dict(x.split('=') for x in query.split('&'))
            if 'query' not in params:
                out = "{\"error\": \"query is required.\"}"
            else:
                out = "{\"result\":\"" + self.llama.run_query(10, self.index, unquote(params.get('query')), self.docs) + "\"}"
            httpd.end_headers()
            httpd.wfile.write(bytes(out, 'utf-8'))
            return
        elif httpd.path == '/health':
            out = "{\"version\": \"" + APP_VERSION + "\"}"
            httpd.end_headers()
            httpd.wfile.write(bytes(out, 'utf-8'))
            return

        root = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'dist')
        logger.info(httpd.path)
        if httpd.path == '/':
            filename = root + '/index.html'
        else:
            filename = root + httpd.path
        httpd.send_response(200)
        if filename[-4:] == '.css':
            httpd.send_header('Content-type', 'text/css')
        elif filename[-5:] == '.json':
            httpd.send_header('Content-type', 'application/javascript')
        elif filename[-3:] == '.js':
            httpd.send_header('Content-type', 'application/javascript')
        elif filename[-4:] == '.ico':
            httpd.send_header('Content-type', 'image/x-icon')
        else:
            httpd.send_header('Content-type', 'text/html')
        httpd.end_headers()
        with open(filename, 'rb') as fh:
            html = fh.read()
            httpd.wfile.write(html)

    def do_POST(self, httpd):
        logger.info(f"self.path: {httpd.path}")
        # curl -F "file=@/Users/dhong/Downloads/11.txt" -F "filename=11.txt" http://localhost:8000/api/upload
        if httpd.path == '/api/upload':
            os.makedirs(UPLOAD_DIR, exist_ok=True)
            ctype, pdict = cgi.parse_header(httpd.headers.get('Content-Type'))
            if ctype == 'multipart/form-data':
                pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
                fields = cgi.parse_multipart(httpd.rfile, pdict)
                file_field = fields.get('file')
                if file_field:
                    filename = httpd.headers['filename'] if 'filename' in httpd.headers else fields['filename'] if 'filename' in fields else 'uploaded_file'
                    if type(filename) is list:
                        filename = filename[0]
                    filepath = os.path.join(UPLOAD_DIR, filename)
                    with open(filepath, 'wb') as output_file:
                        output_file.write(file_field[0])
                    httpd.send_response(200)
                    httpd.send_header("Access-Control-Allow-Origin", ALLOWED_ORIGINS[0])
                    httpd.end_headers()
                    httpd.wfile.write(b"File uploaded successfully")
                else:
                    httpd.send_response(400)
                    httpd.send_header("Access-Control-Allow-Origin", ALLOWED_ORIGINS[0])
                    httpd.end_headers()
                    httpd.wfile.write(b"No file field in request")
            return
        # curl -d '{"filename":"11.txt"}' -H "Content-Type: application/json" -X POST http://localhost:8000/api/load
        elif httpd.path == '/api/load':
            content_length = int(httpd.headers['Content-Length'])
            post_data = httpd.rfile.read(content_length)
            params = json.loads(str(post_data, 'utf-8'))
            shutil.move(UPLOAD_DIR + '/' + params.get('filename'), './local_data/' + params.get('filename'))
            out = 'A file is loaded.'
        # curl -X POST http://localhost:8000/api/reload
        elif httpd.path == '/api/reload':
            if os.path.exists('./index-toy'):
                shutil.rmtree('./index-toy')
            self.llama.build_index()
            self.index, self.docs = self.llama.load_index()
            out = 'index is reloaded'
        # curl -d '{"query":"What does Alec like?"}' -H "Content-Type: application/json" -X POST http://localhost:8000/api/query
        # curl -d '{"query":"Seojun"}' -H "Content-Type: application/json" -X POST http://localhost:8000/api/query
        elif httpd.path == '/api/query':
            content_length = int(httpd.headers['Content-Length'])
            post_data = httpd.rfile.read(content_length)
            params = json.loads(str(post_data, 'utf-8'))
            if 'query' not in params:
                out = 'query is required.'
                httpd.send_response(500)
            else:
                out = self.llama.run_query(3, self.index, params.get('query'), self.docs)
                httpd.send_response(200)
        else:
            out = 'Not found!'
        httpd.protocol_version = 'HTTP/1.0'
        httpd.send_header("Content-type", "application/json")
        httpd.end_headers()
        httpd.wfile.write(bytes("{\"result\":\"" + out + "\"}", 'utf-8'))


