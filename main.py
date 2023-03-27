from flask import Flask,render_template
import csv
from flask_wtf import FlaskForm
from wtforms import StringField,URLField, SelectField,SubmitField
from wtforms.validators import DataRequired,URL
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']


class CafeForm(FlaskForm):
    cafe_name = StringField("Cafe name",validators=[DataRequired()])
    location_url = URLField("Cafe Location in Google Maps (URL)",validators=[DataRequired()])
    open_time = StringField("Opening time eg. 8 AM",validators=[DataRequired()])
    close_time = StringField("Close time eg. 10 PM",validators=[DataRequired()])
    coffee_rating = SelectField("Coffee rating",choices=["☕️","☕️☕️","☕️☕️☕️","☕️☕️☕️☕️","☕️☕️☕️☕️☕️"],validators=[DataRequired()])
    wifi_rating = SelectField("Wifi rating",choices=["✘","💪","💪💪","💪💪💪","💪💪💪💪","💪💪💪💪💪"],validators=[DataRequired()])
    power_outlet = SelectField("Power",choices=["✘","🔌","🔌🔌","🔌🔌🔌","🔌🔌🔌🔌","🔌🔌🔌🔌🔌"],validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route('/')
def home():
    return render_template("index.html")

def read_data():
    with open(r"cafe-data.csv", newline='', encoding="utf-8") as file:
        csv_data = csv.reader(file,delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
        return list_of_rows


@app.route('/add',methods=['GET','POST'])
def add_data():
    form = CafeForm()
    data_list = ["cafe_name","location_url","open_time","close_time","coffee_rating","wifi_rating","power_outlet"]
    new_data = ""
    if form.validate_on_submit():
        cafe_name = form.cafe_name.data
        location_url = form.location_url.data
        open_time = form.open_time.data
        close_time = form.close_time.data
        coffee_rating =form.coffee_rating.data
        wifi_rating =form.wifi_rating.data
        power_outlet = form.power_outlet.data
        new_data = f"{cafe_name},{location_url},{open_time},{close_time},{coffee_rating},{wifi_rating},{power_outlet}"
        with open("cafe_data.csv", 'a', encoding='utf-8') as file:
            file.write(f"\n{new_data}")
        return render_template("cafes.html", cafes = read_data())
    return render_template("add.html",form=form)


@app.route('/cafes')
def cafes_page():
    return render_template("cafes.html",cafes = read_data())



if __name__=="__main__":
    app.run(debug=True)
