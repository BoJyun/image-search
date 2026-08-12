"""
本機開發用的伺服器進入點。
執行方式： python run.py
啟動後開啟 http://localhost:8000
"""
import os
import sys
from http.server import HTTPServer

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT_DIR, 'api'))
from handler import Handler  # noqa: E402

if __name__ == '__main__':
    port = 8000
    server = HTTPServer(('localhost', port), Handler)
    print(f"Serving at http://localhost:{port}")
    server.serve_forever()
