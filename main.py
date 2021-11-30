# developed by Naman Jain contact at namanjain28work@gmail.com or visit https://naman-jain-profile.netlify.app/



from flask import Flask, render_template, request,url_for,redirect
from flask_wtf import FlaskForm
import csv
import os
import pandas as pd
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from flask_bootstrap import Bootstrap
from PIL import Image

class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField(label="Log In")

UPLOAD_FOLDER = 'static'


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
Bootstrap(app)
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'])

# uploads_dir = os.path.join('static')
# uploads_dir1 = os.path.join(app.instance_path, 'static')
# os.makedirs(uploads_dir1)

# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add')
def add_start():
    
    return render_template('add.html')

@app.route('/add_done' ,methods=['GET', 'POST'])
def add_cafe():
    Name = "Data Not Avilable"
    Age = "Data Not Avilable"
    Email = "Data Not Avilable"
    Gender = "Data Not Avilable"
    Interests = "Data Not Avilable"
    Friend_of = "Data Not Avilable"
    if request.method == 'POST':
        Name = request.form['Name']
        
        Age = request.form['Age']
        Email = request.form['Email']
        Gender = request.form['Gender']
        Interests = request.form['Interests']
        Friend_of = request.form['Friend_of']
        id_list = []
        final_id = []
        id = 1
        data = pd.read_csv("\cafe-data.csv", header=None, index_col = False).to_dict()
        data_len_end = int(len(data[0]))
        for a in data[6].values():
            id_list.append(a)
        for i in range(1,data_len_end):
            final_id.append(int(id_list[i]))
        id += (max(final_id))
        profile = request.files['file']
        png_tool = ".png"
        name1 = (f"static/user{id}{png_tool}")
        name = name1
        profile.save((name))
        df = pd.DataFrame({'Name': [Name],
                    'Age': [Age],
                    'Email': [Email],
                    'Gender': [Gender],
                    'Interests': [Interests],
                    'Friend_of': [Friend_of],
                    'id': [id],
                    })
        df.to_csv('\cafe-data.csv', mode='a', index=False, header=False)

    return redirect(url_for('home'))


@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        if login_form.email.data == "admin@email.com" and login_form.password.data == "12345678":
            return redirect(url_for("Users"))
        else:
            return render_template("denied.html")
    return render_template("login.html", form=login_form)

@app.route('/success')
def Users():
    id_list = []
    final_id = []
    id = 1
    name_list = []
    Age_list = []
    Email_list = []
    Gender_list = []
    Interests_list = []

    data = pd.read_csv("\cafe-data.csv", header=None, index_col = False).to_dict()
    data_len_end = int(len(data[0]))
    
    for a in data[0].values():
        name_list.append(a)
    for b in data[1].values():
        Age_list.append(b)
    for c in data[2].values():
        Email_list.append(c)
    for d in data[3].values():
        Gender_list.append(d)
    for e in data[4].values():
        Interests_list.append(e)

    for h in data[6].values():
        id_list.append(h)
    for i in range(1,data_len_end):
        final_id.append(int(id_list[i]))
    id += (max(final_id))
    return render_template("success.html",id=id,id_list=final_id,name_list=name_list,Age_list=Age_list,Email_list=Email_list,Gender_list=Gender_list,Interests_list=Interests_list)

@app.route('/profile/<int:id_value>')
def profile(id_value):
    Name="Name"
    Age="Age"
    Email="Email"
    Gender="Gender"
    Interests="Interests"

    name_list = []
    Age_list = []
    Email_list = []
    Gender_list = []
    Interests_list = []

    data = pd.read_csv("\cafe-data.csv", header=None, index_col = False).to_dict()
    data_len_end = int(len(data[0]))
    
    for a in data[0].values():
        name_list.append(a)
    for b in data[1].values():
        Age_list.append(b)
    for c in data[2].values():
        Email_list.append(c)
    for d in data[3].values():
        Gender_list.append(d)
    for e in data[4].values():
        Interests_list.append(e)

    Name = name_list[id_value]
    Age = Age_list[id_value]
    Email = Email_list[id_value]
    Gender = Gender_list[id_value]
    Interests = Interests_list[id_value]

    return render_template('profile.html', id_value=id_value,Name=Name,Age=Age,Email=Email,Gender=Gender,Interests=Interests)


if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
