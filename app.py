from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    user = {'username': 'Thomas', 'password': 'mypassword'}
    return render_template('index.html', title='Home', user=user)

@app.route("/videos")
def display_videos():
    return render_template('videos.html', title='videos')