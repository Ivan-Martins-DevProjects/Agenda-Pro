from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/api/dashboard", methods=['POST'])
def data():
    return jsonify({
        "message": "Eai"
    })


if __name__ == "__main__":
    app.run(debug=True)
