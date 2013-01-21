import os
from stuff.tomtom import traffic
from flask import render_template
from flask import Flask

app = Flask(__name__)
app.static_folder=os.getcwd() + '/static'

@app.route('/')
def work():
    return render_template('index.html', data=str(traffic('work')))

@app.route('/home')
def home():
    return render_template('index.html', data=str(traffic('hoem')))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)

