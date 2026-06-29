from flask import Flask, jsonify, request

app = Flask(__name__)
counter = 0

@app.route("/")
def home():
    # Get the 'name' parameter from the URL, default to 'Guest' if missing
    username = request.args.get('name', 'Guest')
    return f"Hey {username} welcome! Python Counter API Running!"

@app.route("/count")
def count():
    global counter
    counter += 1
    return jsonify({"count": counter})

app.run(host="0.0.0.0", port=5000) 


