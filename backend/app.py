from flask import Flask, send_file
import os

app = Flask(__name__)


@app.route('/')
def inicio():
    ruta_html = os.path.join(os.path.dirname(__file__), '../frontend/index.html')
    return send_file(ruta_html)


if __name__ == "__main__":
    app.run(debug=True)
