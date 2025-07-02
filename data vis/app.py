from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import json
from sqlalchemy import func
import spacy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from collections import Counter
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres.hxxhlifnneqbbwqvsice:Pa$$w0rd1234!!&&!!@aws-0-eu-west-2.pooler.supabase.com:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

nlp = spacy.load("en_core_web_sm")
geolocator = Nominatim(user_agent="Geocoder")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

class Post(db.Model):
    __tablename__ = 'Posts'
    PostID = db.Column(db.Integer, primary_key=True)
    Content = db.Column(db.String)
    TimeStamps = db.Column(db.DateTime)
    FlaggedStatusID = db.Column(db.Integer)
    ConfirmationStatusID = db.Column(db.Integer, db.ForeignKey('ConfirmationStatus.ConfirmationID'))
    Sentiment = db.Column(db.String)

class ConfirmationStatus(db.Model):
    __tablename__ = 'ConfirmationStatus'
    ConfirmationID = db.Column(db.Integer, primary_key=True)
    MisinformationStatus = db.Column(db.Boolean)

def extract_locations(text):
    doc = nlp(text)
    return [ent.text for ent in doc.ents if ent.label_ == "GPE"]

def geocode_location(location):
    try:
        location = geocode(location)
        return (location.latitude, location.longitude) if location else None
    except Exception as e:
        print(f"Failed to geocode {location}: {str(e)}")
        return None

def extract_keywords(posts):
    all_words = []
    for post in posts:
        doc = nlp(post.Content)
        words = [token.text.lower() for token in doc if not token.is_stop and not token.is_punct and token.is_alpha]
        all_words.extend(words)
    word_freq = Counter(all_words)
    return word_freq.most_common(10)

@app.route('/')
def index():
    posts = Post.query.join(ConfirmationStatus).filter(ConfirmationStatus.MisinformationStatus == True).all()
    keywords = extract_keywords(posts)
    keywords_json = json.dumps(dict(keywords))

    locations = []
    for post in posts:
        for location in extract_locations(post.Content):
            coords = geocode_location(location)
            if coords:
                locations.append({'name': location, 'coordinates': coords})

    locations_json = json.dumps(locations)

    sentiment_counts = db.session.query(
        Post.Sentiment, func.count(Post.Sentiment)
    ).join(ConfirmationStatus).filter(
        ConfirmationStatus.MisinformationStatus == True
    ).group_by(
        Post.Sentiment
    ).all()

    sentiments = [s[0] for s in sentiment_counts]
    sentiment_values = [s[1] for s in sentiment_counts]

    time_counts = db.session.query(
        func.date(Post.TimeStamps).label('date'), 
        func.count('*').label('count')
    ).join(ConfirmationStatus).filter(
        ConfirmationStatus.MisinformationStatus == True
    ).group_by(
        func.date(Post.TimeStamps)
    ).order_by(
        func.date(Post.TimeStamps)
    ).all()

    time_labels = [t.date.strftime('%Y-%m-%d') for t in time_counts]
    time_values = [t.count for t in time_counts]

    return render_template('index.html',
                           sentiments_json=json.dumps(sentiments),
                           sentiment_values_json=json.dumps(sentiment_values),
                           time_labels_json=json.dumps(time_labels),
                           time_values_json=json.dumps(time_values),
                           locations_json=locations_json,
                           keywords_json=keywords_json)

if __name__ == '__main__':
    app.run(debug=True, port=5002)
