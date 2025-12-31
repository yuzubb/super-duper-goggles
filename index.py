import requests

API_TOKEN = 'pdltp_ddf4e09704b297cbe0f6b792d9b5128e94678ec14c991d98b7befc8102ca7555b1c596'

# エンドポイント
url = "https://api.padlet.dev/v1/me"

# ヘッダーの設定
headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

try:
    # GETリクエストの送信
    response = requests.get(url, headers=headers)

    # ステータスコードの確認
    if response.status_code == 200:
        user_info = response.json()
        print("--- 取得したユーザー情報 ---")
        # 取得したい項目（名前、ユーザー名など）を表示
        print(f"Name: {user_info['data']['attributes']['name']}")
        print(f"Username: {user_info['data']['attributes']['username']}")
        print(f"Email: {user_info['data']['attributes']['email']}")
    else:
        print(f"エラーが発生しました。ステータスコード: {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"接続中にエラーが発生しました: {e}")
