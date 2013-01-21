import os
from stuff.tomtom import traffic
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Delay ' + str(traffic('work'))

@app.route('/home')
def hello():
    return 'Delay ' + str(traffic('home')))

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)

