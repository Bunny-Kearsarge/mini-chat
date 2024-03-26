import random
import re
import sys
import threading
import time
from flask import Flask, render_template
from turbo_flask import Turbo

from forms.message import MessageForm

app = Flask(__name__)
app.secret_key = 'secret_key'
turbo = Turbo(app)

messages = ['test', 'Hello, World!', '123']

@app.context_processor
def inject_load():
    return {'messages': messages}


@app.route('/', methods=['GET', 'POST'])
def index():
    form = MessageForm()
    if form.validate_on_submit():
        messages.append(form.text.data)
    return render_template('index.html', form=form)

def update_load():
    with app.app_context():
        while True:
            time.sleep(1)
            turbo.push(turbo.replace(render_template('load_messages.html'), 'load'))


th = threading.Thread(target=update_load)
th.daemon = True
th.start()

app.run()
