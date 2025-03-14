from flask import Flask, render_template, request


app = Flask(__name__)

@app.route('/results/<nickname>/<int:level>/<float:rating>')
def choice(nickname, level, rating):
    return render_template("results_of_otbor.html",
                           nickname=nickname, level=level, rating=rating)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
