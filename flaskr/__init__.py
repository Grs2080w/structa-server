from flask import Flask
from flask_cors import CORS

from flaskr.graphql.server import graphql_Blueprint

app = Flask(__name__)
CORS(
    app,
    resources={r"/*": {"origins": "*"}},
    supports_credentials=True,
    methods=["GET", "POST"],
)

# Routes
app.register_blueprint(graphql_Blueprint)

if __name__ == "__main__":
    app.run()
