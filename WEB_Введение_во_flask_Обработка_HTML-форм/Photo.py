from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
app.config['IMG_FOLDER'] = 'static/img'


@app.route('/sample_file_upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file :
            filename = file.filename
            file.save(os.path.join(app.config['IMG_FOLDER'], filename))
            return redirect(url_for('upload_file', filename=filename))
    return render_template('donwload_photo.html', filename=request.args.get('filename'))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
