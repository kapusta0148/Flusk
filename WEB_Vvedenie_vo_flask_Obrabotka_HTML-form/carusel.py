from flask import Flask, render_template


app = Flask(__name__)

@app.route('/carousel')
def choice():
    return render_template("carusel.html")


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
