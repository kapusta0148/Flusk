from flask import Flask, render_template, request


app = Flask(__name__)

@app.route('/choice/<planet_name>')
def choice(planet_name):
    return render_template("porabotim_mars.html", planet=planet_name)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
