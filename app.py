import datetime
import json
import random
import paddlehub as hub
from flask import Flask, render_template, jsonify, request, make_response, send_from_directory, abort
from werkzeug.utils import secure_filename
from poem.index import *
from user.index import *
from exts import db
import config

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

# readingPicturesWritingPoems = hub.Module(name="reading_pictures_writing_poems")

file_path = ''
poem_text = ''
score = 0.0

def create_uuid():  # 生成唯一的图片的名称字符串，防止图片显示时的重名问题
    nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # 生成当前时间
    randomNum = random.randint(0, 100)  # 生成的随机整数n，其中0<=n<=100
    if randomNum <= 10:
        randomNum = str(0) + str(randomNum)
    uniqueNum = str(nowTime) + str(randomNum)
    return uniqueNum

# def reading_pictures_writing_poem(image_path):
#     result = readingPicturesWritingPoems.WritingPoem(image=image_path, use_gpu=False)
#     return  result

@app.route('/')
def index():
    # print(res)
    return render_template('login.html')

@app.route('/1')
def index2():
    # print(res)
    return render_template('reg.html')

@app.route('/write')
def write():
    # print(res)
    return render_template('write.html')

@app.route('/record')
def record():
    try:
        poems = Poem.query.all()
        print(poems)
        output = []
        for poem in poems:
            output.append(poem.to_json())
        return render_template('record.html', output = output)
    except Exception as e:
        print(e)
        return render_template('record.html')

@app.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    loginUsername = request.form.get('username')
    loginPassword = request.form.get('password')
    print(loginUsername,loginPassword)
    user = User.query.filter_by(name=loginUsername, password=loginPassword).first()
    if user:
        return render_template('write.html')
    return render_template('login.html')

@app.route('/reg', methods=['GET', 'POST'], strict_slashes=False)
def reg():
    loginUsername = request.form.get('username')
    loginPassword = request.form.get('password')
    print(loginUsername,loginPassword)
    user = User(name=loginUsername, password=loginPassword)
    db.session.add(user)
    db.session.commit()
    return render_template('login.html')

@app.route('/shou')
def shou():
    try:
        poems = Poem.query.all()
        print(poems)
        output = []
        for poem in poems:
            output.append(poem.to_json())
        return render_template('shoucang.html', output = output)
    except Exception as e:
        print(e)
        return render_template('shoucang.html')


@app.route('/up_photo', methods=['POST'], strict_slashes=False)
def upload():
    global poem_text, file_path
    try:
        f = request.files['file']
        fname = secure_filename(f.filename)
        ext = fname.rsplit('.', 1)[1]
        filename = create_uuid() + '.' + ext
        path = 'static/up_photo/' + filename
        f.save(path)
        # res = reading_pictures_writing_poem(path)
        file_path = path

        # poem_text = res[0]['Poetrys']

        return jsonify({"code": 0, "poem": poem_text})
    except:
        return jsonify({"code": 1})

@app.route('/save', methods=['POST'], strict_slashes=False)
def save():
    global poem_text, file_path
    time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    try:
        score = json.loads(request.form.get('data'))['score']
        p = Poem(photo_path=file_path, poem=poem_text, score=score, time=time)
        db.session.add(p)
        db.session.commit()
        print(score)
        return jsonify({"code": 1})
    except Exception as e:
        print(e)
        return jsonify({"code": 0})

@app.route('/shoucang', methods=['POST'], strict_slashes=False)
def shoucang():
    try:
        time = json.loads(request.form.get('data'))['time']
        print(time)
        Poem.query.filter_by(time=time).update({"shoucang":1})
        db.session.commit()
        return jsonify({"code": 1})
    except Exception as e:
        print(e)
        return jsonify({"code": 0})


@app.route('/cancel', methods=['POST'], strict_slashes=False)
def cancel():
    try:
        time = json.loads(request.form.get('data'))['time']
        print(time)
        Poem.query.filter_by(time=time).update({"shoucang":0})
        db.session.commit()
        return jsonify({"code": 1})
    except Exception as e:
        print(e)
        return jsonify({"code": 0})

if __name__ == '__main__':
    app.run()

