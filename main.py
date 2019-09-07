from flask import Flask, render_template, request
import datetime
from flask_paginate import Pagination, get_page_args
import pickle

try:
    msgs = pickle.load(open('data.p', 'rb'))
except:
    msgs = []

def add_msg(msgs, msg):
    if len(msgs) < 100:
        msgs.append(msg)
    else:
        del msgs[0]
        msgs.append(msg)
    pickle.dump(msgs, open('data.p', 'wb'))

def get_msgs(offset=0, per_page=5):
    print(msgs[offset: offset + per_page])
    return msgs[offset: offset + per_page]

app = Flask(__name__)

@app.route("/")
def home():
    try:
        msgs = pickle.load(open('data.p', 'rb'))
        print(msgs)
    except:
        msgs = []
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    print(page, per_page, offset)
    total = len(msgs)
    pagination_msgs = get_msgs(offset=page-1, per_page=5)
    pagination = Pagination(page=page, per_page=5, total=total,
                            css_framework='bootstrap4')
    return render_template('home.html', msgs=pagination_msgs,
                                        page=page,
                                        per_page=5,
                                        pagination=pagination,)

@app.route('/', methods=['POST'])
def my_form_post():
    try:
        msgs = pickle.load(open('data.p', 'rb'))
    except:
        msgs = []
    text = request.form['text']
    add_msg(msgs, (text, datetime.datetime.now()))
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    total = len(msgs)
    pagination_msgs = get_msgs(offset=page-1, per_page=5)
    pagination = Pagination(page=page, per_page=5, total=total,
                            css_framework='bootstrap4')
    return render_template('home.html', msgs=pagination_msgs,
                                        page=page,
                                        per_page=5,
                                        pagination=pagination,)

if __name__ == "__main__":
    app.run(debug=True)
