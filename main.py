from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField, CKEditor
from  flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from datetime import datetime
import os


app = Flask(__name__)

# Initialize bootstrap
bootstrap = Bootstrap5(app)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
ckeditor = CKEditor(app)


# This is form contact me
class ContactForm(FlaskForm):
    fullname = StringField(label="Full Name", validators=[DataRequired()])
    email = StringField(label="Email Address", validators=[DataRequired()])
    phone_no = StringField(label="Phone Number", validators=[DataRequired()])
    message = CKEditorField(label="Message", validators=[DataRequired()])
    submit = SubmitField(label="Send")


# This is class to save the data from contact me
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] =  'sqlite:///contact_me.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


class Visitor(db.Model):
    __tablename__ = "visitor_info"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(String(50), unique=True)
    phone_no: Mapped[str] = mapped_column(String(50))
    message: Mapped[str] = mapped_column(Text)

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    year = datetime.today().now().year
    contact_form = ContactForm()
    if contact_form.validate_on_submit():
        new_user = Visitor(username=contact_form.fullname.data,
                           email=contact_form.email.data,
                           phone_no=contact_form.phone_no.data,
                           message=contact_form.message.data)
        db.session.add(new_user)
        db.session.commit()
    return render_template('index.html', year=year, form=contact_form)



if __name__ == "__main__":
    app.run(debug=False)