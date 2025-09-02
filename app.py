from flask import Flask, render_template
import pandas as pd
import os

app = Flask(__name__)

# Get absolute path to CSV
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "flattened_mod_review.csv")

@app.route('/')
def display_applications():
    try:
        # Read CSV with explicit encoding handling
        df = pd.read_csv(CSV_FILE, encoding='utf-8')
        df = df.fillna('')

        # Define excluded columns
        excluded_cols = [
            'Verified Perma/Username', 
            'Reddit username', 
            'Communities', 
            'Karma', 
            'Verified Email?', 
            'Account Age', 
            'Banned?', 
            'Timestamp'
        ]
        
        # Get question columns
        question_columns = [col for col in df.columns if col not in excluded_cols]

        users = []
        for index, row in df.iterrows():
            # Use Reddit username if available, else fallback
            username = str(row['Reddit username']).strip() or str(row['Verified Perma/Username']).strip() or f"Unknown_User_{index}"
            communities = str(row['Communities']).strip() if 'Communities' in df.columns else 'N/A'

            # Build responses list
            responses = []
            for q in question_columns:
                ans = str(row[q]).strip()
                if ans == '' or ans.lower() == 'nan':
                    ans = 'No response'
                responses.append({'question': q, 'answer': ans})

            users.append({
                'user_id': index,
                'username': username,
                'communities': communities if communities else 'N/A',
                'responses': responses
            })

        return render_template('index.html', users=users)

    except Exception as e:
        return f"Error loading CSV file: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
