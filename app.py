from flask import Flask, render_template, request
import openai

# Initialize Flask application
# Flask will handle routing for our RESTful API
app = Flask(__name__)

# Configuration for OpenAI API
class OpenAIConfig:
    def __init__(self):
        # RESTful API endpoint for the local OpenAI-compatible model
        self.base_url = "http://localhost:1234/v1"
        self.api_type = "open_ai"
        self.api_key = "not-needed"

# Function to initiate conversation with the local-model
# This encapsulates the API call logic, adhering to the principle of separation of concerns
def initiate_conversation(input_text, system_message):
    # Make a POST request to the OpenAI API endpoint
    # This follows RESTful conventions: using POST for creating a new resource (in this case, a chat completion)
    response = openai.ChatCompletion.create(
        model="local-model",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": input_text}
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

# Define route for the home page
# This is a GET request, following RESTful conventions for retrieving a resource
@app.route('/')
def home():
    return render_template('index.html')

# Define route for chat functionality
# This is a POST request, following RESTful conventions for creating a new resource (chat message)
@app.route('/chat', methods=['POST'])
def chat():
    # Extract user input from the POST request
    user_input = request.form['user_input']
    system_message = "I'm Allen Sun. You are Aurora Nova. You are Allen's artificial intelligence assistant."
    
    # Call the AI model and get the response
    model_response = initiate_conversation(user_input, system_message)
    
    # Return the response
    # In a more complex RESTful API, we might return a JSON object with additional metadata
    return model_response

if __name__ == '__main__':
    # Instantiate configuration
    config = OpenAIConfig()
    
    # Set up OpenAI API configuration
    # This configures the client to interact with our RESTful API endpoint
    openai.api_base = config.base_url
    openai.api_key = config.api_key
    
    # Run the Flask application
    # This starts the server that will handle incoming RESTful API requests
    app.run(debug=True)

