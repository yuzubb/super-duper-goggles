from flask import Flask, jsonify
import yt_dlp
import platform
import time
from datetime import datetime, timedelta

app = Flask(__name__)
start_time = time.time()

# キャッシュを格納する辞書
# 構造: { "video_id": {"expires": タイムスタンプ, "data": 抽出データ} }
cache = {}
CACHE_DURATION = 8 * 60 * 60  # 8時間を秒に換算

def get_cached_data(video_id, mode):
    """キャッシュがあれば返し、なければ None を返す"""
    cache_key = f"{video_id}_{mode}"
    if cache_key in cache:
        entry = cache[cache_key]
        if time.time() < entry["expires"]:
            return entry["data"]
        else:
            del cache[cache_key] # 期限切れなら削除
    return None

def set_cache_data(video_id, mode, data):
    """データをキャッシュに保存"""
    cache_key = f"{video_id}_{mode}"
    cache[cache_key] = {
        "expires": time.time() + CACHE_DURATION,
        "data": data
    }

@app.route('/info/<video_id>')
def get_info(video_id):
    cached = get_cached_data(video_id, "info")
    if cached: return jsonify({"source": "cache", "data": cached})

    url = f"https://www.youtube.com/watch?v={video_id}"
    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            set_cache_data(video_id, "info", info)
            return jsonify({"source": "network", "data": info})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/stream/<video_id>')
def get_stream(video_id):
    cached = get_cached_data(video_id, "stream")
    if cached: return jsonify({"source": "cache", "data": cached})

    url = f"https://www.youtube.com/watch?v={video_id}"
    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            streams = [{"id": f.get("format_id"), "url": f.get("url"), "res": f.get("resolution")} for f in info.get("formats", [])]
            res_data = {"title": info.get("title"), "streams": streams}
            set_cache_data(video_id, "stream", res_data)
            return jsonify({"source": "network", "data": res_data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/m3u8/<video_id>')
def get_m3u8(video_id):
    cached = get_cached_data(video_id, "m3u8")
    if cached: return jsonify({"source": "cache", "data": cached})

    url = f"https://www.youtube.com/watch?v={video_id}"
    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            m3u8_list = [f for f in info.get("formats", []) if 'm3u8' in f.get('protocol', '')]
            res_data = {"title": info.get("title"), "m3u8_streams": m3u8_list}
            set_cache_data(video_id, "m3u8", res_data)
            return jsonify({"source": "network", "data": res_data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/status/')
def get_status():
    uptime = str(timedelta(seconds=int(time.time() - start_time)))
    status = {
        "server": {
            "uptime": uptime,
            "python": platform.python_version(),
            "now": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        "cache_stats": {
            "cached_items_count": len(cache),
            "cache_keys": list(cache.keys())
        }
    }
    return jsonify(status)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
