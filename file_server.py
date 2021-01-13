from flask import Flask, send_from_directory
app = Flask(__name__)


@app.route('/static/<filename>')
def send_static(filename):
    return send_from_directory('static/cache', filename=filename)


@app.route('/test/')
def test():
    return {"detail": "all is well"}


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
