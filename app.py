from flask import Flask, render_template, redirect, url_for
import json

app = Flask(__name__)


@app.route('/')
def redirect_cafe():
    return redirect(url_for('serve_cafe_page'))


@app.route('/cafe')
def serve_cafe_page():
    return render_template('cafe.html')


@app.route('/summary')
def serve_summary_page():
    return render_template('summary.html')


@app.route('/analysis')
def serve_analysis_page():
    return render_template('analysis.html')


@app.route('/authorities')
def serve_authorities_page():
    return render_template('authorities.html')


@app.route('/user')
def serve_user_page():
    return render_template('user.html')


@app.route('/getSlots')
def serve_slots():
    from random import randint
    slots = [{
        'name': 'Masa ' + str(randint(1, 10)),
        'bill': randint(2, 120),
        'time': randint(0, 120),
        'playerCount': randint(1, 4),
        'extraCount': randint(0, 5)
    } for _ in range(randint(7,10))]

    return render_template('slots.html', slots=slots)


@app.route('/getSlotDetails/<slotName>')
def get_javascript_data(slotName):
    return json.dumps({'name': slotName, 'details': 'this is from backend'})


if __name__ == '__main__':
    app.run()
