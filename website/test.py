from matplotlib import pyplot as plt
from supabase import create_client
import supabase


from datetime import timedelta, datetime

#Supabase
supabase_url = "https://hxxhlifnneqbbwqvsice.supabase.co"
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imh4eGhsaWZubmVxYmJ3cXZzaWNlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTQzMTY1MTQsImV4cCI6MjAyOTg5MjUxNH0.iDC1fo8P9cJxY4rlyKYH7fNvLtXbOmg6AvevIme-NoQ'
supabase = create_client(supabase_url, supabase_key)

two_week_ago = datetime.now() - timedelta(days=14)

# Execute the SQL query
response = supabase.table('Posts').select('*').gt('TimeStamps', two_week_ago).execute()
post_count = response.data[-1]

print(post_count)



response = supabase.table('ConfirmationStatus').select('MisinformationStatus', count='exact').eq('MisinformationStatus', True).execute()
total_misinfo_count = response.count
print(total_misinfo_count)