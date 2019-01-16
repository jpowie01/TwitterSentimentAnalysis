from flask import Flask

from rest import blueprint, endpoints


if __name__ == '__main__':
    app = Flask(__name__)
    app.config['SWAGGER_UI_DOC_EXPANSION'] = 'list'
    app.register_blueprint(blueprint)
    app.run(debug=True)

