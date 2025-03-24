from flask import Flask, render_template


app = Flask(__name__)

@app.route('/list_prof/<list>')
def show_list(list):
    return render_template('Spisok_professiy.html',
                         marker=list)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
