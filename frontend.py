from flask import Flask, request, render_template
from flask.ext.cors import CORS, cross_origin

app = Flask(__name__,
            static_url_path='',
            static_folder='static')

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/', methods=['GET'])
@cross_origin()
def my_form():
    username = request.args.get('username', '')
    if username:
        return render_template('status.html', username=username)
    return render_template('form.html')


@app.route('/', methods=['POST'])
@cross_origin(origin='*')
def my_form_post():
    username = request.form['text']
    return render_template('status.html', username=username)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8522)
