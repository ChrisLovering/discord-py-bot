from flask import Flask, request, send_from_directory
app = Flask(__name__)

@app.route('/static/<filename>')
def send_static(filename):
    return send_from_directory('static/cache', filename=filename)

if __name__ == '__main__':
        app.run(debug=True,host='0.0.0.0')