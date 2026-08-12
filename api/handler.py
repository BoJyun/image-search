"""後端邏輯：路由處理 + 呼叫 Unsplash API。"""
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler

from config import UNSPLASH_ACCESS_KEY

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def search_unsplash(query):
    endpoint = 'https://api.unsplash.com/search/photos?' + urllib.parse.urlencode({
        'query': query,
        'per_page': 12,
    })
    req = urllib.request.Request(endpoint, headers={
        'Authorization': f'Client-ID {UNSPLASH_ACCESS_KEY}',
        'Accept-Version': 'v1',
    })
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode('utf-8'))


class Handler(BaseHTTPRequestHandler):
    def _send_json(self, status, payload):
        body = json.dumps(payload).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in ('/', '/index.html'):
            file_path = os.path.join(ROOT_DIR, 'index.html')
            with open(file_path, 'rb') as f:
                body = f.read()
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path != '/api/search':
            self.send_error(404)
            return

        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode('utf-8')
        params = urllib.parse.parse_qs(body)
        query = params.get('query', [''])[0].strip()

        if not query:
            self._send_json(400, {'error': '請輸入搜尋關鍵字'})
            return

        if UNSPLASH_ACCESS_KEY == 'YOUR_UNSPLASH_ACCESS_KEY':
            self._send_json(500, {'error': '尚未設定 Unsplash Access Key，請在 api/config.py 填入'})
            return

        try:
            data = search_unsplash(query)
        except urllib.error.HTTPError as e:
            try:
                error_payload = json.loads(e.read().decode('utf-8'))
            except json.JSONDecodeError:
                error_payload = {'error': f'Unsplash API 錯誤（HTTP {e.code}）'}
            self._send_json(e.code, error_payload)
            return
        except urllib.error.URLError as e:
            self._send_json(502, {'error': f'無法連線至 Unsplash：{e.reason}'})
            return

        results = [{
            'thumbUrl': photo['urls']['small'],
            'fullUrl': photo['urls']['regular'],
            'alt': photo.get('alt_description') or '',
            'author': photo.get('user', {}).get('name', ''),
            'authorUrl': photo.get('user', {}).get('links', {}).get('html', ''),
        } for photo in data.get('results', [])]

        self._send_json(200, {'results': results})

    def log_message(self, format, *args):
        print(f"{self.address_string()} - {format % args}")
