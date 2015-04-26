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
    #rand
    randNo1 = 0
    randNo2 = 0
    session['voted'] = ""
    obj = db.db()
    count = obj.counts()
    count2 = 0
    if (count[0] % 2) != 0:
        count2 = (count[0]+1)/2
        count2 = count2 - 1
    else:
        count2 = count[0]/2
    while randNo1 == randNo2:
        randNo1 = randint(1,count2)
        randNo2 = randint(count2+1,count[0])
    #obj = db.db()
    v1 = obj.video(randNo1)
    v2 = obj.video(randNo2)
    flag = True
    while flag:
        try:
            h = httplib2.Http()
            resp = h.request(v1[0], 'HEAD')
            assert int(resp[0]['status']) < 400
            flag = False
        except:
            randNo1 = randint(1,count2)
            v1 = obj.video(randNo1)
            flag = True
    flag = True
    while flag:
        try:
            h = httplib2.Http()
            resp = h.request(v2[0], 'HEAD')
            assert int(resp[0]['status']) < 400
            flag = False
        except:
            randNo2 = randint(count2+1,count[0])
            v2 = obj.video(randNo2)
            flag = True
    return render_template('index.html',id1 = randNo1, id2 = randNo2, url1 = v1[0].replace(" ",""), url2 = v2[0].replace(" ",""), ol1 = v1[1].replace(" ",""), ol2 = v2[1].replace(" ",""))

@app.route('/submit', methods = ['GET','POST'])
def submit():
    if request.method == 'POST':
        url = request.form['url']
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
                flag = obj.custom(url)
                if flag:
                    return render_template('submit.html', resp = 'Added to list..')
                else:
                    return render_template('submit.html', resp = 'Oops got some error, try again..')
            except Exception:
                return render_template('submit.html', resp = 'Please check the url..')
        else:
            return render_template('submit.html', resp = 'Enter a valid mp4 url..')
    else:
        return render_template('submit.html', resp = '')

@app.route('/vote')
def vote():
    id = request.args.get('id')
    other = request.args.get('other')
    id = int(id)
    other = int(other)
    obj = db.db()
    flag = obj.votes(id)
    #prev = other
    try:
        if flag:
            if session['voted'] == "":
                session['voted'] = '%d' % id
            else:
                session['voted'] = session['voted'] + '-%d' % id
            randNo1 = 0
            randNo2 = 0
            obj = db.db()
            count = obj.counts()
            count2 = 0
            if (count[0] % 2) != 0:
                count2 = (count[0]+1)/2
                count2 = count2 - 1
            else:
                count2 = count[0]/2
            sr = session['voted'].split('-')
            while (randNo1 == other) or (randNo2 == other) or (str(randNo1) in sr) or (str(randNo2) in sr) or randNo1==randNo2:
                randNo1 = randint(1,count2)
                randNo2 = randint(count2+1,count[0])
            obj = db.db()
            v1 = obj.video(randNo1)
            v2 = obj.video(randNo2)
            flag = True
            while flag:
                try:
                    h = httplib2.Http()
                    resp = h.request(v1[0], 'HEAD')
                    assert int(resp[0]['status']) < 400
                    flag = False
                except:
                    randNo1 = randint(1,count2)
                    while (randNo1 == other) or (str(randNo1) in sr):
                        randNo1 = randint(1,count2)
                    v1 = obj.video(randNo1)
                    flag = True
            flag = True
            while flag:
                try:
                    h = httplib2.Http()
                    resp = h.request(v2[0], 'HEAD')
                    assert int(resp[0]['status']) < 400
                    flag = False
                except:
                    randNo2 = randint(count2+1,count[0])
                    while (randNo2 == other) or (str(randNo2) in sr):
                        randNo2 = randint(count2+1,count[0])
                    v2 = obj.video(randNo2)
                    flag = True
            data = {"status" : 1, "v1": v1[0], "v2": v2[0], "id1" : randNo1, "id2" : randNo2}
            js = json.dumps(data)
            resp = Response(js, status = 200, mimetype = 'application/json')
            return resp
        else:
            data = {"status" : 0, "text": "We got some error.."}
            js = json.dumps(data)
            resp = Response(js, status = 200, mimetype = 'application/json')
            return resp
    except Exception:
        data = {"status" : 0, "text": "We got some error.."}
        js = json.dumps(data)
        resp = Response(js, status = 200, mimetype = 'application/json')
        return resp

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/top')
def top():
    return render_template('top.html')

################flask server################
if __name__ == "__main__":
	app.run(debug=True)
