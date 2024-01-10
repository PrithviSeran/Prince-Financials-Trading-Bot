from flask import Flask, request, jsonify 
from google_main import main


app = Flask(__name__)

@app.route("/deploy-bot/<username>")
def testing(username):
    result = main(username)

    return result, 200


if __name__ == "__main__":
    app.run(debug=True)