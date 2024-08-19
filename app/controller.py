import os
import requests
from app.llama import Llama
import json
import logging
import cgi
from urllib.parse import unquote
import settings

APP_VERSION = '0.2'
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='%(message)s')

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

        content_length = int(httpd.headers['Content-Length'])
        post_data = httpd.rfile.read(content_length)
        params = json.loads(str(post_data, 'utf-8'))
        httpd.send_response(200)

        # curl -X POST http://localhost:8000/api/reload
        if httpd.path == '/api/reload':
            self.index, self.docs = self.llama.reload()
            out = 'Indexes are reloaded!'
        # curl -X POST http://localhost:8000/api/reset
        elif httpd.path == '/api/reset':
            self.index, self.docs = self.llama.reset()
            out = 'Indexes are reset!'
        # curl -d '{"filename":"11.txt"}' -H "Content-Type: application/json" -X POST http://localhost:8000/api/applyidx
        elif httpd.path == '/api/applyidx':
            source = UPLOAD_DIR + '/' + params.get('filename')
            target = settings.INDEX_TMP_DATA_DIR + '/' + params.get('filename')
            self.index, self.docs = self.llama.applyidx(source, target)
            out = 'Indexes are reloaded!'
        # curl -d '{"query":"What does Alec like?"}' -H "Content-Type: application/json" -X POST http://localhost:8000/api/query
        elif httpd.path == '/api/query':
            if 'message' not in params:
                out = 'message is required.'
                httpd.send_response(500)
            else:
                out = self.llama.run_query(3, self.index, params.get('message'), self.docs)
                # out = '111'
        else:
            out = 'API Not found!'
        httpd.send_header('Content-type', 'application/json')
        httpd.end_headers_ext()
        response_json = json.dumps({
            'message': out
        })
        httpd.wfile.write(response_json.encode('utf-8'))



