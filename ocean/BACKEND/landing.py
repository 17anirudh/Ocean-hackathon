from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route("/output.json")
def serve_json():
    return send_from_directory(".", "output.json")

if __name__ == "__main__":
    app.run(debug=True)
