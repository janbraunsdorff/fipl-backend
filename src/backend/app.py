from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@localhost:5432/fipl'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from backend.schema.db_views import db
    db.init_app(app)

    from backend.api.api_group import app_group
    from backend.api.api_account import app_account
    from backend.api.api_transaction import app_transaction
    app.register_blueprint(app_group)
    app.register_blueprint(app_account)
    app.register_blueprint(app_transaction)

    return app


def run():
    create_app().run(debug=True, host='0.0.0.0')


if __name__ == '__main__':
    run()