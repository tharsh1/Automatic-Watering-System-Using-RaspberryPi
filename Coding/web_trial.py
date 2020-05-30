from flask import Flask, render_template, redirect, url_for
import datetime
import water

app = Flask(__name__, template_folder='static')

def template(title = "Automatic Watering System", text = ""):
    now = datetime.datetime.now()
    timeString = now
    templateDate = {
        'title' : title,
        'time' : timeString,
        'text' : text
        }
    return templateDate

@app.route("/")
def hello():
    templateData = template()
    return render_template('main.html', **templateData)

@app.route("/last_watered")
def check_last_watered():
    f = open("pump_off_time.txt","r")
    templateData = template(text = f.readline())
    return render_template('main.html', **templateData)

@app.route("/soil_status")
def action():
    status = water.soil_status()
    message = ""
    if (status == 1):
        message = "Dry"
    else:
        message = "Wet"

    templateData = template(text = message)
    return render_template('main.html', **templateData)

@app.route("/water_once")
def action2():
    water.water_once()
    templateData = template(text = "Watered Once")
    return render_template('main.html', **templateData)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)

