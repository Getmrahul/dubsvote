import os
from flask import Flask, render_template
from random import randint

app = Flask(__name__)

@app.route('/')
def index():
    #rand
    randNo1 = randint(1,250)
    randNo2 = randint(251,500)
    return render_template('index.html')
