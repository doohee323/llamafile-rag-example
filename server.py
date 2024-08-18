from http.server import HTTPServer, SimpleHTTPRequestHandler
import argparse
import http.server
import base64
import logging
from app.controller import Controller
import os
from jproperties import Properties

configs = Properties()
filePath = '.env'
if not os.path.isfile(filePath):
    filePath = '../.env'
with open(filePath, 'rb') as f:
    configs.load(f)
env = configs.properties

auth_realm = env.get('auth_realm')
auth_users = {
    env.get('user'): env.get('password'),
    env.get('dev'): env.get('dev_password'),
}

APP_VERSION = '0.2'
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(message)s')

class AuthHTTPRequestHandler(SimpleHTTPRequestHandler):
    controller = Controller()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def end_headers_ext(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        # and self.server.server_address[0] != '0.0.0.0'
        # username = None
        # if self.path != '/health':
        #     username = self.authenticate()
        #     if username is None:
        #         return
        #     self.username = username
        self.controller.do_GET(self)

    def do_POST(self):
        self.controller.do_POST(self)

    def authenticate(self):
        auth_header = self.headers.get('Authorization')
        if auth_header is None:
            self.send_response(401)
            self.send_header('WWW-Authenticate', f'Basic realm="{auth_realm}"')
            self.end_headers()
            return None

        auth_type, auth_payload = auth_header.split()
        if auth_type != 'Basic':
            return None

        try:
            username, password = base64.b64decode(auth_payload).decode('utf-8').split(':')
        except:
            return None

        if username not in auth_users or password != auth_users[username]:
            self.send_response(401)
            self.send_header('WWW-Authenticate', f'Basic realm="{auth_realm}"')
            self.end_headers()
            return None

        return username


def run(server_class=HTTPServer, handler_class=AuthHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a simple HTTP server")
    parser.add_argument(
        "-l",
        "--listen",
        default="0.0.0.0",  # localhost
        help="Specify the IP address on which the server listens",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=8000,
        help="Specify the port on which the server listens",
    )
    args = parser.parse_args()
    run()
