from flask import Flask, render_template, request
from werkzeug import secure_filename
app = Flask(__name__)

#업로드 HTML 렌더링
@app.route('/upload')
def render_file():
    return render_template('upload.html')

#파일업로드
@app.route('/fileUpload', methods = ['GET','POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']

        f.save('./uploads/' + secure_filename(f.filename))
        return 'uploads 디렉토리 -> 파일 업로드 성공!'

if __name__ == '__main__':
    app.run(debug = True)