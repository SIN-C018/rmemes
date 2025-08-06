from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

# Path to your CSV file
CSV_FILE = "flattened_mod_review.csv"

@app.route('/')
def display_applications():
    try:
        # Read CSV file with proper encoding and handle potential encoding issues
        df = pd.read_csv(CSV_FILE, encoding='utf-8', on_bad_lines='skip')
        print("CSV Columns:", df.columns.tolist())  # Debug: Print column names
        print("Sample Data:", df[['Verified Perma/Username', 'Communities']].head())  # Debug: Print sample data
        # Replace NaN values with empty strings
        df = df.fillna('')
        # Prepare data for template: group by username, handle bad data
        users = []
        question_columns = [col for col in df.columns if col not in ['Verified Perma/Username', 'Reddit username', 'Communities', 'Karma', 'Verified Email?', 'Account Age', 'Banned?', 'Timestamp']]
        for index, row in df.iterrows():
            username = str(row['Verified Perma/Username']).strip()
            if not username or username.lower() in ['true', 'false', 'nan', '']:
                username = str(row['Reddit username']).strip() or f"Unknown_User_{index}"
            communities = str(row['Communities']).strip()
            user_data = {
                'user_id': index,  # Unique ID for each user
                'username': username,
                'communities': communities if communities else 'N/A',
                'responses': [
                    {'question': q, 'answer': str(row[q]).strip() if pd.notna(row[q]) else ''}
                    for q in question_columns
                    if str(row[q]).strip()  # Only include non-empty answers
                ]
            }
            users.append(user_data)
        return render_template('index.html', users=users)
    except Exception as e:
        return f"Error loading CSV file: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
