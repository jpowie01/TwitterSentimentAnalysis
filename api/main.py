from flask import Flask
from flask_cors import CORS

from rest import blueprint, endpoints


if __name__ == '__main__':
    app = Flask(__name__)
    CORS(app)
    app.config['SWAGGER_UI_DOC_EXPANSION'] = 'list'
    app.register_blueprint(blueprint)
    app.run(debug=True)

