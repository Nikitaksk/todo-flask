from flask import Flask
from flask_bcrypt import Bcrypt
from models import db
from routes import main
from s_key import key

app = Flask(__name__)
app.secret_key = key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt = Bcrypt(app)

from auth import auth, login_manager
login_manager.init_app(app)
app.register_blueprint(main)
app.register_blueprint(auth)

if __name__ == '__main__':
    app.run(debug=True)
