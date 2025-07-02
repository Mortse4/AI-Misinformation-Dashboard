from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres.hxxhlifnneqbbwqvsice:Pa$$w0rd1234!!&&!!@aws-0-eu-west-2.pooler.supabase.com:5432/postgres'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Posts(db.Model):
    __tablename__ = 'Posts'
    PostID = db.Column(db.Integer, primary_key=True)
    Content = db.Column(db.String)
    TimeStamps = db.Column(db.DateTime)
    FlaggedStatusID = db.Column(db.Integer)
    ConfirmationStatusID = db.Column(db.Integer)
    Sentiment = db.Column(db.Text)

class FlaggedMisinformation(db.Model):
    __tablename__ = 'FlaggedMisinformation'
    FlaggedID = db.Column(db.Integer, primary_key=True)
    DateFlagged = db.Column(db.DateTime)

class ConfirmationStatus(db.Model):
    __tablename__ = 'ConfirmationStatus'
    ConfirmationID = db.Column(db.Integer, primary_key=True)
    MisinformationStatus = db.Column(db.Boolean)

@app.route('/')
def index():
    posts = Posts.query.filter_by(FlaggedStatusID=None, ConfirmationStatusID=None).order_by(Posts.PostID.asc()).all()
    return render_template('index.html', posts=posts)

@app.route('/flag/<int:post_id>', methods=['POST'])
def flag(post_id):
    misinformation_status = request.form.get('misinformation_status') == 'confirm'
    new_flagged_misinformation = FlaggedMisinformation(DateFlagged=datetime.now())
    new_confirmation_status = ConfirmationStatus(MisinformationStatus=misinformation_status)
    
    db.session.add(new_flagged_misinformation)
    db.session.add(new_confirmation_status)
    db.session.flush()
    
    post_to_update = Posts.query.get(post_id)
    post_to_update.FlaggedStatusID = new_flagged_misinformation.FlaggedID
    post_to_update.ConfirmationStatusID = new_confirmation_status.ConfirmationID
    db.session.commit()
    
    return redirect(url_for('index'))

def get_newsapi_results(query, api_key):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "apiKey": api_key,
        "language": "en",
        "sortBy": "relevance",
        "pageSize": 3
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()['articles']

@app.route('/fetch_research', methods=['POST'])
def fetch_research():
    post_content = request.form['post_content']
    api_key = '10fcb437026e4b9a9fa3f5ff2417e3b5'  # Replace with your actual API key
    try:
        articles = get_newsapi_results(post_content, api_key)
        formatted_articles = atricleformatter(articles)
        return render_template('articles.html', articles=formatted_articles)
    except Exception as e:
        return str(e)

def get_newsapi_results(query, api_key):
    """Fetches articles related to the query using NewsAPI."""
    url = "https://newsapi.org/v2/everything"
    #turn the query into a string
    query = str(query)
    #strip to first 9 words
    query = ' '.join(query.split()[:6])
    #remove any special characters not spaces though
    query = ''.join(e for e in query if e.isalnum() or e.isspace())
    print('aaaaaa',query)
    

    params = {
        "q": query,  # Search query
        "apiKey": api_key,  # API key
        "language": "en",  # Filter articles by language, optional
        "sortBy": "relevance",  # Sort by relevance
        "pageSize": 3  # Limit the number of results to the top 3
    }
    response = requests.get(url, params=params)
    response.raise_for_status()  # Raise an exception for bad requests
    return response.json()['articles']

def atricleformatter(articles):
    """Displays the title, description, and URL of the articles."""
    formatted_articles = []
    for article in articles:
        formatted_articles.append({
            "title": article["title"],
            "description": article["description"],
            "url": article["url"]
        })
    return formatted_articles
    


if __name__ == '__main__':
    app.run(debug=True, port=5001)