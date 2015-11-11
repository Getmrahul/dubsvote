import os
from flask import Flask, render_template, request, Response, session
from random import randint
import db
import json
import httplib2

app = Flask(__name__)
app.secret_key = os.urandom(25)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/videos')
def getVideos():
    try:
        vType = request.args.get("id")
        row = []
        obj = db.db()
        row = obj.videoIds(int(vType))
        randNo1 = 0
        randNo2 = 0
        vids = []
        if not row:
            raise Exception("Video fetch error")
        else:
            for i in row:
                vids.append(int(i[0]))
            count = len(vids)
            count2 = 0
            if (count % 2) != 0:
                count2 = (count+1)/2
                count2 = count2 - 1
            else:
                count2 = count/2
            while randNo1 == randNo2:
                randNo1 = randint(1,count2)
                randNo2 = randint(count2+1,count)
            v1 = obj.video(vids[randNo1])
            v2 = obj.video(vids[randNo2])
            flag = True
            while flag:
                try:
                    h = httplib2.Http()
                    resp = h.request(v1[0], 'HEAD')
                    assert int(resp[0]['status']) < 400
                    flag = False
                except:
                    randNo1 = randint(1,count2)
                    v1 = obj.video(vids[randNo1])
                    flag = True
            flag = True
            while flag:
                try:
                    h = httplib2.Http()
                    resp = h.request(v2[0], 'HEAD')
                    assert int(resp[0]['status']) < 400
                    flag = False
                except:
                    randNo2 = randint(count2+1,count)
                    v2 = obj.video(vids[randNo2])
                    flag = True
            data = {"status" : 1, "url1": v1[0].replace(" ",""), "url2": v2[0].replace(" ",""), "id1" : vids[randNo1], "id2" : vids[randNo2]}
            js = json.dumps(data)
            resp = Response(js, status = 200, mimetype = 'application/json')
            return resp
    except Exception as exp:
        data = {"status" : 0, "text": "We got some error.."}
        js = json.dumps(data)
        print exp
        resp = Response(js, status = 200, mimetype = 'application/json')
        return resp

@app.route('/submit', methods = ['GET','POST'])
def submit():
    if request.method == 'POST':
        url = request.form['url']
        lang = request.form['lang']
        ####Filter
        urlArray = url.split('.')
        if urlArray[len(urlArray)-1].lower() == 'mp4':
            #check if url exist
            try:
                h = httplib2.Http()
                resp = h.request(url, 'HEAD')
                assert int(resp[0]['status']) < 400
                #exists
                obj = db.db()
                flag = obj.custom(url,int(lang))
                if flag:
                    url = obj.videoUrl(url)
                    return render_template('submit.html', resp = 'Added to list..', url = "http://dubsvote.com/dub/"+str(url[0]))
                else:
                    return render_template('submit.html', resp = 'Oops got some error, try again..')
            except Exception as exp:
                print exp
                return render_template('submit.html', resp = 'Please check the url..')
        else:
            return render_template('submit.html', resp = 'Enter a valid mp4 url..')
    else:
        return render_template('submit.html', resp = '')

@app.route('/vote')
def vote():
    try:
        id = request.args.get('id')
        other = request.args.get('other')
        vType = request.args.get('type')
        id = int(id)
        other = int(other)
        obj = db.db()
        flag = obj.votes(id)
        #prev = other
        if flag:
            if 'voted' not in session:
                session['voted'] = str(id)
            else:
                session['voted'] = session['voted'] + '-' + str(id)
            row = []
            row = obj.videoIds(int(vType))
            randNo1 = 0
            randNo2 = 0
            vids = []
            if not row:
                raise Exception("No vid")
            for i in row:
                vids.append(int(i[0]))
            count = len(vids)
            count2 = 0
            if (count % 2) != 0:
                count2 = (count+1)/2
                count2 = count2 - 1
            else:
                count2 = count/2
            sr = session['voted'].split('-')
            while (vids[randNo1] == other) or (vids[randNo2] == other) or (str(vids[randNo1]) in sr) or (str(vids[randNo2]) in sr) or randNo1==randNo2:
                randNo1 = randint(1,count2)
                randNo2 = randint(count2+1,count)
            obj = db.db()
            v1 = obj.video(vids[randNo1])
            v2 = obj.video(vids[randNo2])
            flag = True
            while flag:
                try:
                    h = httplib2.Http()
                    resp = h.request(v1[0], 'HEAD')
                    assert int(resp[0]['status']) < 400
                    flag = False
                except:
                    randNo1 = randint(1,count2)
                    while (vids[randNo1] == other) or (str(vids[randNo1]) in sr):
                        randNo1 = randint(1,count2)
                    v1 = obj.video(vids[randNo1])
                    flag = True
            flag = True
            while flag:
                try:
                    h = httplib2.Http()
                    resp = h.request(v2[0], 'HEAD')
                    assert int(resp[0]['status']) < 400
                    flag = False
                except:
                    randNo2 = randint(count2+1,count)
                    while (vids[randNo2] == other) or (str(vids[randNo2]) in sr):
                        randNo2 = randint(count2+1,count)
                    v2 = obj.video(vids[randNo2])
                    flag = True
            data = {"status" : 1, "v1": v1[0], "v2": v2[0], "id1" : vids[randNo1], "id2" : vids[randNo2]}
            js = json.dumps(data)
            resp = Response(js, status = 200, mimetype = 'application/json')
            return resp
        else:
            data = {"status" : 0, "text": "We got some error.."}
            js = json.dumps(data)
            resp = Response(js, status = 200, mimetype = 'application/json')
            return resp
    except Exception as exp:
        data = {"status" : 0, "text": "We got some error.."}
        print exp
        js = json.dumps(data)
        resp = Response(js, status = 200, mimetype = 'application/json')
        return resp

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/top')
def top():
    return render_template('top.html')

@app.route('/top/feed')
def topFeed():
    obj = db.db()
    data = []
    data = obj.topVideos(20)
    videoLinks = ""
    videoIds = ""
    if not data:
        data = {"status" : 0, "text": "We got some error.."}
        js = json.dumps(data)
        resp = Response(js, status = 200, mimetype = 'application/json')
        return resp
    else:
        for id in data:
            vid = int(id[0])
            try:
                v = obj.video(vid)
                if videoLinks == "":
                    videoLinks = videoLinks + v[0].replace(" ","")
                    videoIds = videoIds + str(id[0])
                else:
                    videoLinks = videoLinks + '|-|'+ v[0].replace(" ","")
                    videoIds = videoIds + '|-|'+ str(id[0])
            except Exception:
                vidtest = False
        data = {"status" : 1, "links": videoLinks, "ids": videoIds}
        js = json.dumps(data)
        resp = Response(js, status = 200, mimetype = 'application/json')
        return resp

@app.route('/dub/<id>')
def indVid(id):
    try:
        id = int(id)
        obj = db.db()
        row = []
        row = obj.video(id)
        if not row:
            data = {"status" : 0, "text": "404"}
            js = json.dumps(data)
            resp = Response(js, status = 404, mimetype = 'application/json')
            return resp
        else:
            return render_template('templates.html',url=row[0].replace(" ",""), id = id)
    except Exception:
        data = {"status" : 0, "text": "We got some error.."}
        js = json.dumps(data)
        resp = Response(js, status = 200, mimetype = 'application/json')
        return resp

@app.route('/dub/vote')
def dubVote():
    try:
        id = request.args.get("id")
        obj = db.db()
        ids = str(id)
        id = int(id)
        if ids in session:
            data = {"status" : 0, "text": "Already voted."}
            js = json.dumps(data)
            resp = Response(js, status = 200, mimetype = 'application/json')
            return resp
        else:
            flag = obj.votes(id)
            if flag:
                session[ids] = 1
                data = {"status" : 1, "text": "Thanks for the vote."}
                js = json.dumps(data)
                resp = Response(js, status = 200, mimetype = 'application/json')
                return resp
            else:
                data = {"status" : 0, "text": "We got some error.."}
                js = json.dumps(data)
                resp = Response(js, status = 200, mimetype = 'application/json')
                return resp
    except Exception as exp:
        data = {"status" : 0, "text": "We got some error.."}
        js = json.dumps(data)
        print exp
        resp = Response(js, status = 200, mimetype = 'application/json')
        return resp

@app.route('/dub/frame/<id>')
def iframe(id):
    try:
        id = int(id)
        obj = db.db()
        row = []
        row = obj.video(id)
        if not row:
            data = {"status" : 0, "text": "404"}
            js = json.dumps(data)
            resp = Response(js, status = 404, mimetype = 'application/json')
            return resp
        else:
            return '<iframe src="'+row[0].replace(" ","")+'" width="100%" height="100%">No Support</iframe>'
    except Exception:
        data = {"status" : 0, "text": "We got some error.."}
        js = json.dumps(data)
        resp = Response(js, status = 200, mimetype = 'application/json')
        return resp

################flask server################
if __name__ == "__main__":
	app.run(debug=True)
