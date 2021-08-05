from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import youtube_dl
import requests
import os
import to_srt
from to_txt import to_txt, xml_to_txt
import to_auto_srt

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
# https://www.youtube.com/watch?v=HPsazrVSjl8


def get_video_info(video_url):
    ydl_opts = {}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        video_info = ydl.extract_info(video_url, download=False)
    return video_info


@app.route('/video-info')
def index():
    video_url = request.args.get('url')
    ydl_opts = {}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        video_info = ydl.extract_info(video_url, download=False)
    return jsonify(video_info)


@app.route('/manual_srt_download')
def manual_srt_download():
    video_url = request.args.get('url')
    lang = request.args.get('lang')
    video_info = get_video_info(video_url)
    video_title = video_info['title']
    video_vtt_file_name = f'{video_title}[Checksub.com]'
    ydl_opts = {
        'writesubtitles': True,
        'skip_download': True,
        'subtitleslangs': [lang],
        'outtmpl': f'./{video_vtt_file_name}'
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
        to_srt.main()
    temp = send_file(f'./{video_title}[Checksub.com].{lang}.vtt.srt', as_attachment=True)
    os.remove(f'./{video_title}[Checksub.com].{lang}.vtt.srt')
    os.remove(f'./{video_title}[Checksub.com].{lang}.vtt')
    return temp


@app.route('/manual_txt_download')
def manual_txt_download():
    video_url = request.args.get('url')
    lang = request.args.get('lang')
    video_info = get_video_info(video_url)
    video_title = video_info['title']
    video_vtt_file_name = f'{video_title}[Checksub.com]'
    ydl_opts = {
        'writesubtitles': True,
        'skip_download': True,
        'subtitleslangs': [lang],
        'outtmpl': f'./txt/{video_vtt_file_name}'
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
        to_txt()
    temp = send_file(f'./txt/{video_title}[Checksub.com].{lang}.txt', as_attachment=True)
    os.remove(f'./txt/{video_title}[Checksub.com].{lang}.vtt')
    os.remove(f'./txt/{video_title}[Checksub.com].{lang}.txt')
    return temp


@app.route('/automatic_srt_download')
def automatic_srt_download():
    video_url = request.args.get('url')
    lang = request.args.get('lang')
    video_info = get_video_info(video_url)
    video_title = video_info['title']
    video_xml_url = video_info['automatic_captions'][lang][0]['url']
    resource = requests.get(video_xml_url, allow_redirects=True)
    new = resource.content.replace(b"&#39;", bytes("'", encoding='utf8'))
    video_xml_file = f'./xml/{lang}{video_title}[Checksub.com].xml'
    open(video_xml_file, 'wb').write(new)
    to_auto_srt.main(f'./xml/{lang}{video_title}[Checksub.com].xml', f'./xml/{lang}{video_title}[Checksub.com].srt')
    temp = send_file(f'./xml/{lang}{video_title}[Checksub.com].srt', as_attachment=True)
    os.remove(f'./xml/{lang}{video_title}[Checksub.com].srt')
    os.remove(f'./xml/{lang}{video_title}[Checksub.com].xml')
    return temp


@app.route('/automatic_txt_download')
def automatic_txt_download():
    video_url = request.args.get('url')
    lang = request.args.get('lang')
    video_info = get_video_info(video_url)
    video_title = video_info['title']
    video_xml_url = video_info['automatic_captions'][lang][0]['url']
    resource = requests.get(video_xml_url, allow_redirects=True)
    new = resource.content.replace(b"&#39;", bytes("'", encoding='utf8'))
    video_xml_file = f'./txt/{video_title}[Checksub.com].xml'
    open(video_xml_file, 'wb').write(new)
    video_txt_file = f'./txt/{video_title}[Checksub.com].txt'
    xml_to_txt(video_xml_file, video_txt_file)
    temp = send_file(f'./txt/{video_title}[Checksub.com].txt', as_attachment=True)
    os.remove(f'./txt/{video_title}[Checksub.com].xml')
    os.remove(f'./txt/{video_title}[Checksub.com].txt')
    return temp


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not---- Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
