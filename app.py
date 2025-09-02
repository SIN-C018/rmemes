from flask import Flask, render_template
import pandas as pd
import os

app = Flask(__name__)

# Get absolute path to CSV file (always works)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "flattened_mod_review.csv")

@app.route('/')
def display_applications():
    try:
        # Read CSV file safely
        df = pd.read_csv(CSV_FILE, encoding='utf-8', on_bad_lines='skip')
        df = df.fillna('')  # Replace NaN values with empty strings

        # Identify question columns (ignore metadata)
        excluded_columns = [
            'Verified Perma/Username', 'Reddit username', 'Communities',
            'Karma', 'Verified Email?', 'Account Age', 'Banned?', 'Timestamp'
        ]
        question_columns = [col for col in df.columns if col not in excluded_columns]

        # Build structured user data
        users = []
        for index, row in df.iterrows():
            username = str(row['Verified Perma/Username']).strip()
            if not username or username.lower() in ['true', 'false', 'nan', '']:
                username = str(row['Reddit username']).strip() or f"Unknown_User_{index}"

            user_data = {
                'user_id': index,
                'username': username,
                'communities': str(row['Communities']).strip() or 'N/A',
                'responses': [
                    {'question': q, 'answer': str(row[q]).strip()}
                    for q in question_columns if str(row[q]).strip()
                ]
            }
            users.append(user_data)

        return render_template('index.html', users=users)

    except Exception as e:
        return f"Error loading CSV file: {str(e)}"


if __name__ == '__main__':
    app.run(debug=True)
