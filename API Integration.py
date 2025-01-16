from flask import Flask, request, jsonify

app = Flask (__name__)

@app.route("/")

def home():
    return "1. Main Menu\n2. Services\n3. About"
    
if __name__ == "__main__":
    app.run(debug=True)