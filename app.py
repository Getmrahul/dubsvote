import os
from flask import Flask, render_template
from random import randint
import db

app = Flask(__name__)

@app.route('/')
def index():
    #rand
    randNo1 = randint(1,255)
    randNo2 = randint(256,510)
    obj = db.db()
    v1 = obj.video(randNo1)
    v2 = obj.video(randNo2)
    return render_template('index.html', url1 = v1[0], url2 = v2[0], ol1 = v1[1], ol2 = v2[1])

################flask server################
if __name__ == "__main__":
	app.run(debug=True)
