import os
from stuff.tomtom import traffic
from flask import render_template
from flask import Flask
import settings

app = Flask(__name__)
app.static_folder=os.getcwd() + '/static'
cost_per_day = round(float(settings.work_miles*2/settings.miles_per_gallon*settings.cost_per_gallon),3)


def debug_enabled():
    return os.environ.get('MORNING_DEBUG', '').lower() in ('1', 'true', 'yes', 'on')

@app.route('/')
def work():
	return render_template('index.html', data=str(traffic('work')), transport=cost_per_day, news=str(settings.news))

@app.route('/home')
def home():
    return render_template('index.html', data=str(traffic('hoem')))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=debug_enabled())
