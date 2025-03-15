from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/astronaut_selection', methods=['POST', 'GET'])
def astronaut_selection():
    if request.method == 'GET':
        return render_template("html_anketa.html")
    elif request.method == 'POST':
        surname = request.form['surname']
        name = request.form['name']
        email = request.form['email']
        education = request.form['class']
        professions = request.form.getlist('profession')
        gender = request.form['sex']
        about = request.form['about']
        photo = request.files['file']
        ready_for_mars = 'accept' in request.form
        print(f"Фамилия: {surname}")
        print(f"Имя: {name}")
        print(f"Email: {email}")
        print(f"Образование: {education}")
        print(f"Профессии: {', '.join(professions)}")
        print(f"Пол: {gender}")
        print(f"О себе: {about}")
        print(f"Фото: {photo.filename}")
        print(f"Готов остаться: {'Да' if ready_for_mars else 'Нет'}")

        return "Форма успешно отправлена!"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)