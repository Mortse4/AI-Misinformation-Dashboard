from matplotlib import pyplot as plt
from supabase import create_client
import supabase


from datetime import timedelta, datetime

#Supabase
supabase_url = "https://hxxhlifnneqbbwqvsice.supabase.co"
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imh4eGhsaWZubmVxYmJ3cXZzaWNlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTQzMTY1MTQsImV4cCI6MjAyOTg5MjUxNH0.iDC1fo8P9cJxY4rlyKYH7fNvLtXbOmg6AvevIme-NoQ'
supabase = create_client(supabase_url, supabase_key)

#Get bi-weekly sentiment from table
def get_sentiment_count(supabase, sentiment, two_week_ago):
        response = supabase.table('Posts') \
                        .select('ConfirmationStatusID, Sentiment, TimeStamps, ConfirmationStatus:ConfirmationStatusID!inner(ConfirmationID, MisinformationStatus)', count='exact') \
                        .eq('ConfirmationStatus.MisinformationStatus', True) \
                        .eq('Sentiment', sentiment) \
                        .gt('TimeStamps', two_week_ago) \
                        .execute()
        return response.count


    # Create bar plot for bi-weekly sentiments
def plot_sentiment(categories,counts):
    plt.bar(categories, counts, color=['#DB374D', '#f7b635', '#416EEC'])
    plt.xlabel('Sentiment')
    plt.ylabel('Number of Post')
    plt.title('Bi-Weekly Misinformation Post: Sentiment Distribution')
   

    # Save the plot as an image
    plt.savefig('static/images/sentiment_distribution.png')

    # Close the plot to free up memory
    plt.close()


two_week_ago = datetime.now() - timedelta(days=14)

# Query and filter graphs
neg_count = get_sentiment_count(supabase, 'Negative', two_week_ago)
pos_count = get_sentiment_count(supabase, 'Positive', two_week_ago)
neut_count = get_sentiment_count(supabase, 'Neutral', two_week_ago)

# Data
categories = ['Negative', 'Neutral', 'Positive']
counts = [neg_count, neut_count, pos_count]

plot_sentiment(categories, counts)