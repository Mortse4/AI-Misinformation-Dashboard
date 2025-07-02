from functools import wraps
from flask import Flask, render_template, redirect, request, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from supabase import create_client
from wtforms import SubmitField, StringField, IntegerField, TextAreaField
from flask_bootstrap import Bootstrap
from wtforms.validators import DataRequired, Length
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import subprocess

import matplotlib.pyplot as plt
import subprocess


app = Flask(__name__)

# photos = UploadSet('photos', IMAGES)
app.config['SECRET_KEY'] = 'top secret!kdsfidfoshfpwieu8t04dhofsp'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
bootstrap = Bootstrap(app)



#Supabase
supabase_url = "https://hxxhlifnneqbbwqvsice.supabase.co"
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imh4eGhsaWZubmVxYmJ3cXZzaWNlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTQzMTY1MTQsImV4cCI6MjAyOTg5MjUxNH0.iDC1fo8P9cJxY4rlyKYH7fNvLtXbOmg6AvevIme-NoQ'
supabase = create_client(supabase_url, supabase_key)

# configure_uploads(app, photos)

db = SQLAlchemy(app)


#Table for graphs
#Table for graphs
class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    dataGathered = db.Column(db.Integer)
    likesTotal = db.Column(db.Integer)
    commentsTotal = db.Column(db.Integer)
    sharesTotal = db.Column(db.Integer)
    interactions = db.Column(db.Integer)
    date = db.Column(db.Integer)
    desc = db.Column(db.String(500))
    image = db.Column(db.String(100))




# ------------------------ FORMS HERE -----------------------------


class AddTopic(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 16)])
    dataGathered = IntegerField('Interactions', validators=[DataRequired()])
    interactions = IntegerField('Interactions', validators=[DataRequired()])
    likesTotal = IntegerField('Likes', validators=[DataRequired()])
    sharesTotal = IntegerField('shares', validators=[DataRequired()])
    commentsTotal = IntegerField('comments', validators=[DataRequired()])
    desc = TextAreaField('Description', validators=[DataRequired(), Length(max=500)])
    date = StringField('Date', validators=[DataRequired()])
    image = StringField('Image', validators=[DataRequired()])

    Add = SubmitField('Submit')



class Report(FlaskForm):
    misinfo_link = StringField('Misinformation Link:', validators=[DataRequired()])
    source_link = StringField('Source Link:', validators=[DataRequired()])
    details = TextAreaField('Details:', validators=[DataRequired()])
    

@app.route('/run_new_app', methods=['POST'])
def run_new_app():
    # Run the new Flask app using subprocess
    subprocess.Popen(['python', 'Article Confirmation/app.py'])
    return redirect(url_for('index'))  # Redirect to some other endpoint after running the new app


@app.route('/', methods=['GET', 'POST'])
def index():
    #Fetch supabase data from within this week and parse 
    two_week_ago = datetime.now() - timedelta(days=14)

    graphs_response = supabase.table('graphs').select('*').gt('date', two_week_ago).execute()
    graphs = graphs_response.data

    sorted_flag = True



    #Queries for the weekly data gathered and verified
    misinformation_response = supabase.table('Posts') \
                            .select('ConfirmationStatusID, TimeStamps, ConfirmationStatus:ConfirmationStatusID!inner(ConfirmationID, MisinformationStatus)', count='exact') \
                            .eq('ConfirmationStatus.MisinformationStatus', True) \
                            .gt('TimeStamps', two_week_ago) \
                            .execute()
    misinfo_count = misinformation_response.count

    verified_response = supabase.table('Posts') \
                            .select('ConfirmationStatusID, Sentiment, TimeStamps, ConfirmationStatus:ConfirmationStatusID!inner(ConfirmationID)', count='exact') \
                            .gt('TimeStamps', two_week_ago) \
                            .execute()
    verified_count = verified_response.count

    post_response = supabase.table('Posts') \
                            .select('*', count='exact') \
                            .gt('TimeStamps', two_week_ago) \
                            .execute()
    post_count = post_response.count
    post_time = post_response.data[0]
    
    report_form = Report()
    if request.method == 'POST':
        # Retrieve form data
        misinfo_link = request.form['misinfo-link']
        source_link = request.form['source-link']
        details = request.form['Details']
        
        # Process form data, for example, print it
        print("Misinformation Link:", misinfo_link)
        print("Source Link:", source_link)
        print("Details:", details)
        
        # Add your code to save form data to a database or perform other actions
        
        # Redirect to a thank you page or render a success message
        return redirect(url_for('thanks'))

    

    return render_template('index.html', graphs=graphs, sorted_flag=sorted_flag, 
                           misinfo_count=misinfo_count, 
                           verified_count=verified_count,
                           post_count=post_count,
                           post_time=post_time,
                           )



@app.route('/graph/<id>')
def graph(id):
    graphs_response = supabase.table('graphs').select('*').order('date', desc=True).execute()
    graphs = graphs_response.data

    graph_response = supabase.table('graphs').select('*').eq('id', id).execute()
    graph = graph_response.data[0]
  
    sorted_flag = True
    

    #Alltime Icons container
    response = supabase.table('Posts').select('*', count='exact').execute()
    post_count = response.count
    

    verified_response = supabase.table('Posts') \
                            .select('ConfirmationStatusID, Sentiment, TimeStamps, ConfirmationStatus:ConfirmationStatusID!inner(ConfirmationID)', count='exact') \
                            .execute()
    verified_count = verified_response.count

    response = supabase.table('ConfirmationStatus').select('MisinformationStatus', count='exact').eq('MisinformationStatus', True).execute()
    misinformation_count = response.count

    return render_template('view-graph.html', graph=graph, graphs=graphs, sorted_flag=sorted_flag, 
                                                post_count=post_count, 
                                                verified_count=verified_count,
                                                misinformation_count=misinformation_count)



@app.route('/sort/<string:sortby>')
def sortGraphs(sortby):

    
    if sortby == 'name' :
        query = supabase.table('graphs').select('*').order('name', desc=False).execute()
        graphs = query.data
        sorted_flag = True
    elif sortby == 'date':
        query = supabase.table('graphs').select('*').order('name', desc=True).execute()
        graphs = query.data
        query = supabase.table('graphs').select('*').order('name', desc=True).execute()
        graphs = query.data
        sorted_flag = True
  

    return render_template('graphs.html', graphs=graphs, sorted_flag=sorted_flag)
    return render_template('graphs.html', graphs=graphs, sorted_flag=sorted_flag)



@app.route('/thanks', methods=['GET', 'POST'])
def thanks():
     return render_template('thanks.html')





@app.route('/graphs', methods=['GET', 'POST'])
def graphs():
    # Fetch all graphs from Supabase
    response = supabase.table('graphs').select('*').execute()
    graphs = response.data

    
    return render_template('graphs.html', graphs=graphs)













# ------------- Admin STARTS HERE ---------------
def check_password(password):
     
    SpecialSym = ['$', '@', '#', '%', 
                  '!', '&', '*', '^', '~']
    # checks if the password meets the following criteria
    if len(password) < 6:
         return False
         
    if len(password) > 20:
        return False
         
    if not any(char.isdigit() for char in password):
         return False
         
    if not any(char.isupper() for char in password):
         return False
         
    if not any(char.islower() for char in password):
        return False
         
    if not any(char in SpecialSym for char in password):
        return False
    # returns the value of val if all the criteria are met
    return True



@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        if check_password(password) == False:
            return render_template("admin/signup.html", error="Inadequate password, please include at least one uppercase letter, one lowercase letter, one numeral, and one of the following symbols: $@#%^&*~!")
            
            
        
        # Create new user in Supabase
        response = supabase.auth.sign_up({"email": email, "password": password})
        
        
        if response: 
            return redirect("login")
        
    return render_template("admin/signup.html")





@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        
        # Authenticate user with Supabase
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        
        if response:
            session["user_id"] = response.user.id
            return redirect("/profile")
      
    return render_template("admin/login.html")

@app.route("/profile")
def profile():
    # Retrieve user ID from session
    user_id = supabase.auth.get_session()
   
    user_data = supabase.auth.get_user()
        
    return render_template("profile.html", user=user_data)



@app.route('/admin', methods=['GET', 'POST'])
def admin():
    form = AddTopic()

    if form.validate_on_submit():

        
        # Create new record in Supabase
        new_graph = {
            'name': form.name.data,
            'dataGathered': form.dataGathered.data,
            'interactions': form.interactions.data,
            'likesTotal': form.likesTotal.data,
            'sharesTotal': form.sharesTotal.data,
            'commentsTotal': form.commentsTotal.data,
            'image': form.image.data
        }
        response = supabase.from_('graphs').insert([new_graph]).execute()

 
    # Retrieve graphs from Supabase
    response = supabase.from_('graphs').select('*').execute()
    return render_template('admin/admin.html', admin=True, form=form, graphs=graphs)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_graph(id):
    graph = Topic.query.get_or_404(id)
    form = AddTopic(request.form, obj=graph)
    if form.validate_on_submit():
        form.populate_obj(graph)
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('admin/editTopics.html', form=form, graph=graph)

@app.route('/deleteTopic/<int:id>', methods=['POST'])
def deleteTopic(id):
    graph = Topic.query.get_or_404(id)
    db.session.delete(graph)
    db.session.commit()
    return redirect(url_for('admin'))









if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
