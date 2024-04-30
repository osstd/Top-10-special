from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('F_KEY')
URL = os.environ.get("URL")


def get_top_10(date):
    response = requests.get(url=f"{URL}/{date}/")
    billboard_html = response.text
    soup = BeautifulSoup(billboard_html, "html.parser")
    find_all_tracks = soup.find_all(class_="o-chart-results-list-row-container")
    tracks = [track for track in find_all_tracks]
    song_list = []
    for track in tracks[:10]:
        track_dict = {'title': track.find(id='title-of-a-story').text.strip(),
                      'img': track.select_one('img.lrv-u-width-100p')['data-lazy-src']}
        song_list.append(track_dict)
    return song_list


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get10', methods=['POST'])
def get10():

    print(request.form['date'])
    date = request.form['date']
    song_list = get_top_10(date)
    return render_template('results.html', list=song_list)


if __name__ == '__main__':
    app.run(debug=False)
