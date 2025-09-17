from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from models import db
from routes import messages_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)
app.register_blueprint(messages_bp)

if __name__ == '__main__':
    app.run(port=5555)