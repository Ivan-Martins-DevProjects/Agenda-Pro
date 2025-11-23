from flask import Flask, jsonify
from src.validation import *
from src.handlers import dashboard

SetupLogging()

app = Flask(__name__)

@app.route("/api/dashboard", methods=['POST'])
def data():
    resultado = dashboard.main()

    return jsonify(resultado)

if __name__ == "__main__":
    app.run(debug=True)
