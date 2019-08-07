from flask import Flask,request,redirect, url_for, render_template, flash
from flask.json import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user,\
    current_user
from oauth import OAuthSignIn



functions = Flask(__name__)
functions.config['SECRET_KEY'] = 'top secret!'
functions.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
functions.config['OAUTH_CREDENTIALS'] = {
    'github': {
        'id': '4d08ab3b69881a406b10',
        'secret': '37ce557dccd9537b46eead4866e847a7bb6074f9'
    }
 }







db = SQLAlchemy(functions)
lm = LoginManager(functions)
lm.login_view = 'homepage'


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True)




@lm.user_loader
def load_user(id):
    return User.query.get(int(id))



@functions.route('/')
def index():
    return render_template('homepage.html')


@functions.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('homepage'))


@functions.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('homepage'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@functions.route('/login/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('homepage'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('homepage'))
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, nickname=username, email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('homepage'))




@functions.route('/sum/<int:a>/<int:b>',methods = ["GET"])
def sum(a,b):
	answer = a+b
	return jsonify(answer)


@functions.route('/multiply/<int:a>/<int:b>/<int:c>',methods = ["GET"])
def multiply(a,b,c):
	answer = a*b*c
	return jsonify(answer)



@functions.route('/divide/<int:a>/<int:b>/<int:c>',methods = ["GET"])
def divide(a,b,c):
	answer = a/b/c
	return jsonify(answer)



@functions.route('/modulus/<int:a>/<int:b>',methods = ["GET"])
def modulus(a,b):
	answer = a%b
	return jsonify(answer)


if __name__ == '__main__':
	db.create_all()
	functions.run(debug = True)






