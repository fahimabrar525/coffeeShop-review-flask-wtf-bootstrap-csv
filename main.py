import csv

from flask import Flask, render_template, url_for, request, redirect
from wtforms import Form, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
app.config["SECRET_KEY"] = "any secret key"


class DetailsForm(FlaskForm):
    cafe = StringField('Cafe Name', validators=[DataRequired()])
    location = StringField('Cafe Location on Google Maps(URL)', validators=[DataRequired()])
    opening = StringField('Opening Time e.g. 8AM', validators=[DataRequired()])
    closing = StringField('Closing Time e.g. 9PM', validators=[DataRequired()])
    submit = SubmitField(label="Submit")


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/cafes')
def cafes():
    return render_template('cafes.html')


@app.route('/add', methods=["POST", "GET"])
def add():
    details_form = DetailsForm()
    if details_form.validate_on_submit():
        data = request.form
        with open('file_append.csv', 'w', newline='') as file:
            fieldnames = ['column1', 'column2', 'column3', 'column4']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'column1': data['cafe'], 'column2': data['location'], 'column3': data['opening'], 'column4': data['closing']})
        return render_template('cafes.html', data=data)
    return render_template('add.html', form=details_form)


if __name__ == "__main__":
    app.run(debug=True)