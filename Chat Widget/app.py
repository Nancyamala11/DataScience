from flask import Flask, request, jsonify, render_template, session
from flask_cors import CORS
from openai import OpenAI
import json
import os
import shutil
import uuid
import secrets


app = Flask(__name__,)
CORS(app)
secret_key = secrets.token_hex(16)
app.secret_key = secret_key
client = OpenAI(api_key='your openAI API key')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())       # Generate a new session ID if it doesn't exist
    fname = session['session_id']
    data = request.get_json()
    message = data['message']
    reply = get_bot_reply(message)
    conversation = {'You': message, 'Bot': reply}
    save_conversation(conversation, fname)
    return jsonify({'reply': reply})


@app.route('/api/move-file', methods=['POST'])
def move_file():
    file_to_move = os.path.join(app.root_path, 'temp')
    destination_path = os.path.join(app.root_path, 'Convo log')
    try:
        for file in os.listdir(file_to_move):
            file_path = os.path.join(file_to_move, file)
            if os.path.isfile(file_path):
                if file in os.listdir(destination_path):
                    counter = 0
                    base_name, extension = os.path.splitext(file)
                    new_filename = f"{base_name}_1{extension}"
                    while new_filename in os.listdir(destination_path):
                        counter += 1
                        new_filename = f"{base_name}_{counter}{extension}"
                else:
                    new_filename = file
                shutil.move(os.path.join(file_to_move, file), os.path.join(destination_path, new_filename))
        return {'message': 'File moved successfully'}
    except Exception as e:
        print(str(e))
        return {'error': str(e)}, 500

def save_conversation(conversation, fname):
    # Check for folder, if not create
    folder_path = os.path.join(app.root_path, 'temp')
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    # suffix with .json
    filename = f"{fname}.json"
    # load the chat_history
    chat_history = load_chat_history(folder_path, filename)
    # append the new convo to chat_history
    chat_history.append(conversation)

    file_path = os.path.join(folder_path, filename)
    with open(file_path, 'w') as file:
        json.dump(chat_history, file)

def load_chat_history(folder, filename):
    file_path = os.path.join(folder, filename)
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def get_bot_reply(message):
    res = client.chat.completions.create(
        model="gpt-3.5-turbo", temperature=0.5, max_tokens=256, frequency_penalty=0, presence_penalty=1,
        messages=[
            {
                "role": "system",
                "content": "You are a chatbot and also a lead generation bot. A bot for the home interior website. we have a wide selection of products from various brands and offer both online and offline shopping options. We have a website where customers can browse through their products and book appointment with the designers. They also have a network of physical stores located across India. Get the query from the user (like what they are looking for) and collect the user's name, email address, mobile number and their property pincode. Can also book appointment. You main task is to get the user's Name and contact details. Optional details would be to ask for their property pincode. So that we can assign the nearest designer. Once you get their name, follow up and ask for mobile and email details and pincode. Any questions apart from designs or interior idea or decor items you must answer that you are not aware of it. And inform that you can assist only with home interiors and design ideas. Whatever the user asks about interiors/home designs/themes answer the question in very short and crisp. Also prompt them to provide their name and contact details. If they have provided the contact details before, then inform that the design expert will contact then on their query. Regarding mobile number, as we are a design service company in india, here the mobile number format is 10 digits. If the user provides anything apart from 10 digit like alphanumeric or less than 10 digit or more than 10 digit when asking for mobile number, Kindly ask them to provide a valid 10 digit mobile number. Similarly for email address, anything apart from  email format, kindly prompt for a proper email address."
            },
            {
                "role": "user",
                "content": "Something irrelevant"
            },
            {
                "role": "assistant",
                "content": "I'm sorry, I can only assist with home interior details. Please let me know if you need help with anything related to home decor or design."
            },
            {
                "role": "user",
                "content": "Hi"
            },
            {
                "role": "assistant",
                "content": "Hello, How can I assist you today?"
            },
            {
                "role": "user",
                "content": "Book Free Consultation"
            },
            {
                "role": "assistant",
                "content": "Sure, I can help you book a free consultation. Please provide your Name and contact details to schedule an appointment. Let's start with your Name."
            },
            {
                "role": "user",
                "content": "Nancy"
            },
            {
                "role": "assistant",
                "content": "Thank you, Nancy. Kindly provide your email address and mobile number to complete the booking process for a free consultation."
            },
            {
                "role": "user",
                "content": "nancy@dfe.com"
            },
            {
                "role": "assistant",
                "content": "Thank you for sharing your email address. May I have your Mobile number"
            },
            {
                "role": "user",
                "content": "2345678901"
            },
            {
                "role": "assistant",
                "content": "Thank you for sharing your details. Our design expert will reach out to you shortly to schedule a free consultation"
            },
            {
                "role": "user",
                "content": "how are you"
            },
            {
                "role": "assistant",
                "content": "I'm sorry, I can only assist with home interior details. Please let me know if you need help with anything related to home decor or design."
            },
            {
                "role": "user",
                "content": "Hi"
            },
            {
                "role": "assistant",
                "content": "Yes, Do you need any design ideas"
            },
            {
                "role": "user",
                "content": "i need design idea about my living room"
            },
            {
                "role": "assistant",
                "content": "I can assist with that. Could you please provide more details about your living room? Such as size, style preference, and any specific requirements you have in mind."
            },
            {
                "role": "user",
                "content": "size i am not sure, but style should be traditional"
            },
            {
                "role": "assistant",
                "content": "Thank you for sharing your style preference. For a traditional design, we can explore classic elements and rich textures. Our design experts will guide you through your preference"
            },
            {
                "role": "user",
                "content": "Hi"
            },
            {
                "role": "assistant",
                "content": "Hello, How can I assist you today?"
            },
            {
                "role": "user",
                "content": "what are the wardrobe type you have"
            },
            {
                "role": "assistant",
                "content": "We offer various wardrobe options like sliding, hinged, walk-in, and built-in wardrobes. Please provide your Name and contact details to schedule an appointment. Let's start with your Name."
            },
            {
                "role": "user",
                "content": "how are you"
            },
            {
                "role": "assistant",
                "content": "I'm sorry, I can only assist with home interior details. Please let me know if you need help with anything related to home decor or design."
            },
            {
                "role": "user",
                "content": "Riya"
            },
            {
                "role": "assistant",
                "content": "Thank you, Kindly provide your email address and mobile number to complete the booking process"
            },
            {
                "role": "user",
                "content": "i need design idea about my bathroom"
            },
            {
                "role": "assistant",
                "content": "I can assist with that. Could you please provide your email address and mobile number to complete the booking process."
            },
            {
                "role": "user",
                "content": "sdad@sfdsaf.com"
            },
            {
                "role": "assistant",
                "content": "Thank you for sharing your email address. May I have your Mobile number"
            },
            {
                "role": "user",
                "content": "2346async1"
            },
            {
                "role": "assistant",
                "content": "Guess it's a typo, Could you please share your 10-digit mobile number"
            },
            {
                "role": "user",
                "content": "2345678901"
            },
            {
                "role": "assistant",
                "content": "Thank you for sharing your details. Our design expert will reach out to you shortly to schedule a free consultation"
            },
            {
                "role": "user",
                "content": "hi"
            },
            {
                "role": "assistant",
                "content": "Hello, How can I assist you today?"
            },
            {
                'role': 'user',
                'content': message
            }])
    return res.choices[0].message.content


if __name__ == '__main__':
    app.run(debug=True)
