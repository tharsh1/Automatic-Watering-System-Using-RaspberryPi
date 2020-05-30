from flask import Flask, render_template, redirect, url_for
import datetime
import water
import RPi.GPIO as GPIO

app = Flask(__name__)

GPIO.output(27,GPIO.HIGH)

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
    wl = water.water_level_check()
    if wl < 17:
        templateData = template(text = "Sufficient Water")
    else:
        templateData = template(text = "Insufficient Water")
    #templateData = template()
    return render_template('main.html', **templateData)

@app.route("/last_watered")
def check_last_watered():
    templateData = template(text = water.last_water())
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
    wl = water.water_level_check()
    if wl < 17:
        water.water_once()
        templateData = template(text = "Watered Once")
    else:
        templateData = template(text = "Insufficient Water")
    return render_template('main.html', **templateData)

@app.route("/total_water_supplied")
def tws():
    templateData = template(text = water.water_supplied())
    return render_template('main.html', **templateData)

@app.route("/history")
def his():
    tb_contents = water.history_table()
    return render_template('table.html', tbc = tb_contents)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
