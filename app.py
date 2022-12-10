from flask import Flask, render_template, request, redirect, make_response, url_for, session
import bcrypt, requests, json
from pprint import pprint
app = Flask(__name__)
app.secret_key = 'b82a1e838e624950964a782d9aeba700'

url_blobStorage = "https://notnetflixsa.blob.core.windows.net"
url_getAllUsers = "https://prod-13.uksouth.logic.azure.com:443/workflows/afcf813dc6e240e6820e86719ccb115d/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=FS6ZSityUWTK0i-fgzAGU6bIio3TuaCPerpTQOzaf-I"
url_newUser = "https://prod-02.uksouth.logic.azure.com:443/workflows/649722d34a2d4922963e285d55d4b447/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=qZ3dVRExANDmduRnSjkAH7rsRsn47hoG0ikBfmdnE-I"
url_getAllVideos = "https://prod-05.uksouth.logic.azure.com:443/workflows/f9a7caec30ba469987b0cfcff112cf23/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=dOx6rGmAcUzMD_V1FMLMQjFfHfjWrDj0bRmH1YQvWsk"
url_getCreatorVideos = "https://prod-18.uksouth.logic.azure.com:443/workflows/b50552e02312482bb85d9417268a3254/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=mN0hDaa17s_7VETv4dw8NmQmgwQ289VG7ofo7qAjzdw"
url_newVideo = "https://prod-06.uksouth.logic.azure.com:443/workflows/cebf405888b34305a918cbeb56b5d9ac/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=KR5HOZzmQkqpfjAuHKw4u1zgG9n8UsPqbiOBeA4wc4Q"
url_getVideoMetadata = "https://prod-08.uksouth.logic.azure.com:443/workflows/3a45c171809745c897f698b83dc31852/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=q7ODOYEVsbX7VOEDf-GVR8MjkQi31uKINpCks5Lc65s"
url_newComment = "https://prod-11.uksouth.logic.azure.com:443/workflows/4aee4be966fc4078b4f94cb64fa29ef9/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=rI0x8Vi9G0y8Bw7B46lK7FwjU34IC8Aw6J2SgPVQs_A"
url_getLikeDislike = "https://prod-02.uksouth.logic.azure.com:443/workflows/868bf0ec46ad4bedaa030074686c2207/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=zZ3ouwqWrN8EcNpI-psyb20h9iAvyWfe1b8UccbQLDM"
url_newLikeDislike = "https://prod-29.uksouth.logic.azure.com:443/workflows/d2303974386244f8ae6855101a14e4a4/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=3zmHAR0CT3tgwpE3CvaSym3_N339MaCMId0ylz7cjbI"

######  LOGIN / SIGN UP  ######
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if 'userId' in session:
        if session['userType'] == 'consumer':
            return redirect(url_for('consumer_dashboard'))
        elif session['userType'] == 'creator':
            return redirect(url_for('creator_dashboard'))
        else:
            session.pop('userId', None)
            session.pop('username', None)
            session.pop('userType', None)
            return redirect(url_for('login'))
    
    if request.method == 'POST':
        msg = None
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        response = requests.get(url_getAllUsers)
        if response.status_code != 200:
            msg="error response code " + str(response.status_code)
            return render_template('signup.html', msg=msg)
        user_records = response.json()['value']
        for user in user_records:
            if user['username'] == username:
                msg = 'Username already exists'
                return render_template('signup.html', msg=msg)
        if password1 != password2:
            msg = 'Passwords do not match'
            return render_template('signup.html', msg=msg)

        password_hash = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
        user_data = {
            'username': username,
            'password': password_hash.decode('utf-8'),
            'usertype': 'consumer'
        }
        body = json.loads(json.dumps((user_data)))
        response = requests.post(json=body, url=url_newUser)
        return render_template('signup_success.html')
        
    return render_template('signup.html')

@app.route("/", methods=['GET', 'POST'])
@app.route("/login", methods=['GET', 'POST'])
def login():
    if 'userId' in session:
        if session['userType'] == 'consumer':
            return redirect(url_for('consumer_dashboard'))
        elif session['userType'] == 'creator':
            return redirect(url_for('creator_dashboard'))
        else:
            session.pop('userId', None)
            session.pop('username', None)
            session.pop('userType', None)
            return redirect(url_for('login'))

    if request.method == "POST":
        msg = None
        username = request.form.get('username')
        password = request.form.get('password')
        response = requests.get(url_getAllUsers)
        if response.status_code != 200:
            msg="error response code " + str(response.status_code)
            return render_template('login.html', msg=msg)
        user_records = response.json()['value']
        for user in user_records:
            if user['username'] == username:
                if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                    session['userId'] = user['id']
                    session['username'] = user['username']
                    session['userType'] = user['usertype']
                else:
                    msg = 'Wrong password'
                    return render_template('login.html', msg=msg)
                if session['userType'] == 'consumer':
                    return redirect(url_for('consumer_dashboard'))
                elif session['userType'] == 'creator':
                    return redirect(url_for('creator_dashboard'))
                else:
                    session.pop('userId', None)
                    session.pop('username', None)
                    session.pop('userType', None)
                    return redirect(url_for('login'))
        msg = 'User not found'
        return render_template('login.html', msg=msg)
    
    return render_template('login.html')

@app.route("/logout", methods=['GET'])
def logout():
    if 'userId' in session:
        session.pop('userId', None)
        session.pop('username', None)
        session.pop('userType', None)
        return render_template('logout_success.html')
    else:
        return redirect(url_for('login'))


######  CONSUMER INTERFACE  ######
@app.route("/consumer/dashboard", methods=['GET'])
def consumer_dashboard():
    if 'userId' not in session or session['userType'] != 'consumer':
        return redirect(url_for('login'))

    response = requests.get(url_getAllVideos)
    metadata = []
    if response.status_code == 200:
        metadata = response.json()['value']

    return render_template("consumer_dashboard.html", metadata=metadata, urlBlob=url_blobStorage, username=session['username'])

@app.route("/consumer/watch/<video_id>", methods=['GET', 'POST'])
def consumer_watch_video(video_id):
    if 'userId' not in session or session['userType'] != 'consumer':
        return redirect(url_for('login'))

    msg = {}
    
    if request.method == "POST":
        ### add new comment
        comment_metadata = {
            'userid' : session['userId'],
            'username' : session['username'],
            'videoid' : video_id,
            'commentContent' : request.form.get('comment')
        }
        comment_response = requests.post(data=comment_metadata, url=url_newComment)
        if comment_response.status_code != 200:
            msg['comment'] = "Unable to post comment: response code " + str(comment_response.status_code)
    
    ### fetch video content & comments to display
    video_response = requests.get(headers={ "videoid": video_id }, url=url_getVideoMetadata)
    metadata = {}
    comments = []
    if video_response.status_code == 200:
        metadata = video_response.json()['video']['value'][0]
        comments_data = video_response.json()['comments']['value']
        for comment in comments_data:
            comments.append(comment)
        if not metadata:
            msg['video'] = "Video not found!"
        else:
            metadata['filepath'] = url_blobStorage + metadata['filepath']
    else:
        msg['video']=f"Could not get the video information: code {video_response.status_code}"

    ### fetch like/dislike data to display
    like_response = requests.get(headers={ 'userId': session['userId'], 'videoId': video_id }, url=url_getLikeDislike)
    likeDislike = {}
    if like_response.status_code == 200:
        likeDislike = like_response.json()
    else:
        msg['likedislike']=f"Could not get the like/disklike information: code {like_response.status_code}"


    return render_template("consumer_watch_video.html", session=session, metadata=metadata, comments=comments, likeDislike=likeDislike, msg=msg)

@app.route("/video/likeDislike", methods=["POST"])
def update_like_dislike():
    if "userId" not in session or session["userType"] != "consumer":
        return redirect()
    
    video_id = request.headers.get('videoId')
    type = request.headers.get('type')
    stored_type = request.headers.get('storedType')
    updated_likeCount = int(request.headers.get('likeCount'))
    updated_dislikeCount = int(request.headers.get('dislikeCount'))

    ### update like/dislike data in Azure CosmosDB
    data = {
        'type': type,
        'userId': session['userId'],
        'videoId': video_id
    }
    response = requests.post(data=data, url=url_newLikeDislike)
    if response.status_code == 200:
        ### return updated data to page
        if stored_type == '' and type == 'like':
            updated_likeCount += 1
        elif stored_type == '' and type == 'dislike':
            updated_dislikeCount += 1
        elif stored_type == 'like' and type == '':
            updated_likeCount -= 1
        elif stored_type == 'like' and type == 'dislike':
            updated_likeCount -= 1
            updated_dislikeCount += 1
        elif stored_type == 'dislike' and type == '':
            updated_dislikeCount -= 1
        elif stored_type == 'dislike' and type == 'like':
            updated_dislikeCount -= 1
            updated_likeCount += 1

    return { 'likeCount': updated_likeCount, 'dislikeCount': updated_dislikeCount }


######  CREATOR INTERFACE  ######
@app.route("/creator/dashboard")
def creator_dashboard():
    if "userid" in session:
        userid = session["userid"]
        username = session["username"]
        usertype = session["usertype"]
        if usertype != "creator":
            return redirect(url_for("login"))
        
        msg = None
        user_data = { "userid": userid }
        response = requests.get(headers=user_data, url=url_getCreatorVideos)

        video_links = []
        if response.status_code == 200:
            videos_metadata = response.json()['value']
            for metadata in videos_metadata:
                video_links.append({ "videoid": metadata['id'], "url" : url_blobStorage + metadata['filepath']})
            if len(video_links) < 1:
                msg="oops, you dont have any videos yet. Upload a video to start sharing now."
        else:
            msg=f"There was an error finding your videos: code {response.status_code}"

        return render_template("creator_dashboard.html", video_links=video_links, msg=msg, username=username)

    return redirect(url_for("login"))

@app.route("/creator/watch")
def creator_watch_video():
    if "userid" in session:
        userid = session["userid"]
        username = session["username"]
        usertype = session["usertype"]
        if usertype != "creator":
            return redirect(url_for("login"))
        
        user_data = { "userid": userid }
        response = requests.get(headers=user_data, url=url_getCreatorVideos)

@app.route("/creator/add_video", methods=["POST", "GET"])
def creator_add_video():
    if "userid" in session:
        userid = session["userid"]
        username = session["username"]
        usertype = session["usertype"]
        if usertype != "creator":
            return redirect(url_for("login"))

        if request.method == "POST":
            video_metadata = {
                "userID": userid,
                "userName": username,
                "title": request.form.get("title"),
                "publisher": request.form.get("publisher"),
                "producer": request.form.get("producer"),
                "genre": request.form.get("genre"),
                "ageRating": request.form.get("ageRating")
            }
            file = {
                "file": ("video.mp4", request.files['file'].stream, "video/mp4")
            }
            response = requests.post(data=video_metadata, files=file, url=url_newVideo)

            if response.status_code != 200:
                msg = "error response code " + str(response.status_code)
                return render_template('creator_add_video.html', msg=msg)
            else:
                return render_template('creator_add_video_success.html')
        
        return render_template("creator_add_video.html", username=username)

    return redirect(url_for("login"))