from flask import Flask, jsonify
import os
import requests

app = Flask(__name__)

@app.route('/')
def get_me_and_display():
    # [cite_start]環境変数からトークンを取得 [cite: 2]
    padlet_token = os.environ.get('PADLET_TOKEN')
    
    if not padlet_token:
        return "エラー: VercelのSettingsで PADLET_TOKEN を設定してください。", 500

    # [cite_start]Padlet APIへリクエスト [cite: 2]
    url = 'https://api.padlet.dev/v1/me'
    headers = {'X-Padlet-Token': padlet_token}

    try:
        [cite_start]response = requests.get(url, headers=headers) [cite: 2]
        [cite_start]data = response.json() [cite: 2]
        
        # 実行結果を画面に出力するためのHTML
        return f"""
        <html>
            <head><title>Padlet User Info</title></head>
            <body>
                <h1>Padlet実行結果</h1>
                <pre>{data}</pre> 
            </body>
        </html>
        """
    except Exception as e:
        return f"実行エラー: {str(e)}", 500

# [cite_start]Vercel用のハンドラ [cite: 2, 3]
def handler(environ, start_response):
    return app(environ, start_response)
