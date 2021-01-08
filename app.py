from flask import Flask, render_template
from wtform_fields import *
from models import *

# Configure app
app = Flask(__name__)
app.secret_key = 'my key'

# Configure database
app.config['SQLALCHEMY_DATABASE_URI']='postgres://shsklsgbuuqmxe:9771ea1cb9a8ce516946709d8a3d1d3ff0fed6ed2af29d40f839b552cb22f78a@ec2-50-19-32-202.compute-1.amazonaws.com:5432/d3ddp9t4foo8th'
db = SQLAlchemy(app)

@app.route("/", methods=['GET', 'POST'])
def index():
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        # check if username exists
        user_object = User.query.filter_by(username=username).all()
        if user_object:
            return "Username not available"
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return "Inserted into DB"

    return render_template("index.html", form=reg_form)


if __name__ == "__main__":
    app.run(debug=True)