from flask import Flask, render_template, jsonify, request
import os
from dotenv import load_dotenv
import requests
import json
from flask_socketio import SocketIO, emit

load_dotenv()

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="http://127.0.0.1:5000")

#Azure bot details
APP_ID = os.getenv("APP_ID") 
APP_PASSWORD = os.getenv("APP_PASSWORD")
DIRECT_LINE_SECRET = os.getenv("DIRECT_LINE_SECRET")
DIRECT_LINE_URL = "https://directline.botframework.com/v3/directline/conversations"

@app.route('/')
def index():
    return render_template('index.html')

# starts chat with bot and grab convo ID
def start_chat():
    headers = {"Authorization": f"Bearer {DIRECT_LINE_SECRET}"}
    response = requests.post(DIRECT_LINE_URL, headers=headers)
    
    if response.status_code != 200:
        print("Error starting chat:", response.json())
        return None
    
    return response.json()["conversationId"]

# sends chat to the bot using chat id
def send_message_to_bot(chat_id, message):
    headers = {
        "Authorization": f"Bearer {DIRECT_LINE_SECRET}",
        "Content-Type": "application/json"
    }
    data = {"type": "message", "from": {"id": "user"}, "text": message}
    response = requests.post(f"{DIRECT_LINE_URL}/{chat_id}/activities", headers=headers, json=data)
    
    if response.status_code != 200:
        print("Error starting chat:", response.json())
        return {"activities": []}
    
    return response.json()

@socketio.on("send_message")
def handle_send_message(data):
    chat_id = start_chat()
    user_message = data["message"]
    bot_response = send_message_to_bot(chat_id, user_message)
    
    #check if bot response contains 'activities' to prevent errors
    if 'activities' in bot_response and bot_response["activities"]:
        emit("bot_response", bot_response)
    else:
        emit("bot_response", {"activities": [{"text": "Bot did not respond."}]})
    
if __name__ == '__main__':
    socketio.run(app, debug=True)
    