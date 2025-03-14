from flask import Flask, render_template


app = Flask(__name__)

@app.route('/')
def mission_name():
    return 'Миссия Колонизация Марса'


@app.route('/index')
def mission_motto():
    return 'И на Марсе будут яблони цвести!'


@app.route('/promotion')
def promotion():
    text = ['Человечество вырастает из детства.',
            'Человечеству мала одна планета.',
            'Мы сделаем обитаемыми безжизненные пока планеты.',
            'И начнем с Марса!',
            'Присоединяйся!']
    return '</br>'.join(text)


@app.route('/image_mars')
def image_mars():
    return render_template("Mars.html")

@app.route("/promotion_image")
def promotion_image():
    return render_template("promotion_mars.html")


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)