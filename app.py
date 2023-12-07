from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import google.generativeai as palm

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

# Define a user database (you can replace this with an actual database)
user_database = {
    'Tenzin Wosel': '12345678'  # Replace with real username and hashed password
}

# Set up your API key
palm.configure(api_key='AIzaSyAMURdYGezrWT4Qqj2UPfBusiM85_hBDnE') 

# List available models and their supported methods
models = palm.list_models()

# Choose a model that supports generateText
model = None
for m in models:
    if 'generateText' in m.supported_generation_methods:
        model = m.name
        break

if model is None:
    raise ValueError("No suitable model found for generateText.")

# Initialize the chat history (global variable for simplicity, consider using a database)
chat_history = []

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check credentials (replace this with your user database lookup)
        if username in user_database and user_database[username] == password:
            session['logged_in'] = True
            session['username'] = username  # Store the username in the session
            return redirect(url_for('chatbot'))
        else:
            return render_template('login.html', message='Invalid login credentials')

    return render_template('login.html')

# Chatbot route
@app.route('/chatbot')
def chatbot():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    # Get the username from the session
    username = session.get('username')

    return render_template('chatbot.html', username=username)

# API route for chatbot interactions
@app.route('/api/healthcare-chatbot', methods=['POST'])
def healthcare_chatbot():
    if not session.get('logged_in'):
        return jsonify({"response": "Please log in to access the chatbot."})

    user_message = request.json['message']

    # Add user input to chat history
    chat_history.append(f"You, {session['username']}: {user_message}")

    # Generate a response from the selected model
    completion = palm.generate_text(
        model=model,
        prompt='\n'.join(chat_history),  # Include the entire chat history as a prompt
        temperature=0.5,
        max_output_tokens=1000,
    )

    # Check if the completion or its result is None
    if completion is None or completion.result is None:
        return jsonify({"response": "I'm sorry, but I couldn't generate a response to that. Please try a different question."})

    # Extract the chatbot's response
    bot_response = completion.result.split('\n')[-1] if completion.result else "No response from the chatbot"

    # Add bot response to chat history
    chat_history.append(f"{bot_response}")

    return jsonify({"response": bot_response})

if __name__ == '__main__':
    app.run(debug=True)
