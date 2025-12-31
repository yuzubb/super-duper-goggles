from http.server import BaseHTTPRequestHandler
import json
import os
import urllib.request

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 環境変数からトークンを取得
        padlet_token = os.environ.get('PADLET_TOKEN')
        
        # Padlet APIへリクエストを飛ばす
        url = 'https://api.padlet.dev/v1/me'
        req = urllib.request.Request(url)
        req.add_header('X-Padlet-Token', padlet_token)

        try:
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                
                # 成功時のレスポンス
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*') # CORS許可
                self.end_headers()
                self.wfile.write(json.dumps(data).encode())
        
        except Exception as e:
            # エラー時のレスポンス
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())
