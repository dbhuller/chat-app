from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from wtform_fields import *
from models import *

# Configure app
app = Flask(__name__)
app.secret_key = 'my key'

# Configure database
app.config['SQLALCHEMY_DATABASE_URI']='postgres://shsklsgbuuqmxe:9771ea1cb9a8ce516946709d8a3d1d3ff0fed6ed2af29d40f839b552cb22f78a@ec2-50-19-32-202.compute-1.amazonaws.com:5432/d3ddp9t4foo8th'
db = SQLAlchemy(app)

# configure flask login
login = LoginManager(app)
login.init_app(app)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route("/", methods=['GET', 'POST'])
def index():
    reg_form = RegistrationForm()
    # Update database if validation is successful
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        # hashed password
        hashed_password = pbkdf2_sha256.hash(password)

        # Add user to DB
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash('Registered Successfully, please Login.', 'success')
        return redirect(url_for('login'))

    return render_template("index.html", form=reg_form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    # allow loign if validation success
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)
        return redirect(url_for('chat'))
    
    return render_template("login.html", form=login_form)

@app.route("/chat", methods=['GET', 'POST'])
# @login_required
def chat():
    if not current_user.is_authenticated:
        flash('Please Login.', 'danger')
        return redirect(url_for('login'))
    return "Chat with me"

@app.route("/logout", methods=['GET'])
def logout():
    logout_user()
    flash('You have logged out successfully.', 'success')
    return redirect(url_for('login'))    


if __name__ == "__main__":
    app.run(debug=True)