from flask import Flask
from flask_cors import CORS
from routes import api

app = Flask(__name__)
CORS(app)
app.register_blueprint(api)

if __name__ == "__main__":
    app.run(debug=True)
