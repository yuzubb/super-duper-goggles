from flask import Flask, jsonify
import os
import requests

app = Flask(__name__)

# ルートパス (https://〜.vercel.app/)
@app.route('/')
def home():
    return "Padlet API Proxy is running. Access /api/me for your info."

# 自分の情報を取得するルート (https://〜.vercel.app/api/me)
@app.route('/api/me')
def get_me():
    padlet_token = os.environ.get('PADLET_TOKEN')
    
    if not padlet_token:
        return jsonify({"error": "Environment variable PADLET_TOKEN is not set"}), 500

    url = 'https://api.padlet.dev/v1/me'
    headers = {'X-Padlet-Token': padlet_token}

    try:
        response = requests.get(url, headers=headers)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Vercel用のハンドラ
def handler(event, context):
    return app(event, context)
