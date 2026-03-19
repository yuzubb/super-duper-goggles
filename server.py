from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/info', methods=['GET'])
def get_stream_info():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"error": "No URL provided"}), 400

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # 動画情報の抽出（ダウンロードはしない）
            info = ydl.extract_info(video_url, download=False)
            
            # 必要な情報（ステータス）を整理
            formats = []
            for f in info.get('formats', []):
                formats.append({
                    'format_id': f.get('format_id'),
                    'extension': f.get('ext'),
                    'resolution': f.get('resolution'),
                    'vcodec': f.get('vcodec'),
                    'acodec': f.get('acodec'),
                    'url': f.get('url'), # これがストリーミングURL
                    'filesize_approx': f.get('filesize_approx')
                })

            response = {
                'title': info.get('title'),
                'duration': info.get('duration'),
                'uploader': info.get('uploader'),
                'view_count': info.get('view_count'),
                'formats': formats
            }
            return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # A-shell内では localhost:5000 で起動
    app.run(host='0.0.0.0', port=5000)
