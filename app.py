from flask import Flask, jsonify

app = Flask(__name__)

@app.route ("/")
def home():
    return jsonify({"message" : "hello"})

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True)