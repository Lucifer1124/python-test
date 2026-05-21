from flask import Flask, jsonify
app = Flask(__name__)
counter = 0
@app.route("/")
def home():
        return "Python Counter API Running!"
@app.route("/count")
def count():
        global counter
        counter += 1
        return jsonify({"count": counter})
app.run(host="0.0.0.0", port=5000)

