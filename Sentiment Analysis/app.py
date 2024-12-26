from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from keywords import keyword_definitions
import difflib

app = Flask(__name__)
CORS(app)

# function to get keyword definition with fuzzy matching
def get_keyword_def(user_message):
    keywords = keyword_definitions.keys()
    
    closest_match = difflib.get_close_matches(user_message.lower(), keywords, n=1, cutoff=0.6)
    
    if closest_match:
        return keyword_definitions[closest_match[0]]
    else:
        return "Definition not found."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    print(f"user message: {user_message}")
    
    bot_response = get_keyword_def(user_message)
    print(f"Bot response: {bot_response}")
    return jsonify({"response": bot_response})

# # Custom route to serve static HTML files
# @app.route('/static/HTML/<filename>')
# def custom_static(filename):
#     return app.send_static_file(f'HTML/{filename}')

if __name__ == '__main__':
    app.run(debug=True)
    
