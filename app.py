from flask import Flask, render_template, request
import openai

app = Flask(__name__)

# Configuration for OpenAI API
class OpenAIConfig:
    def __init__(self):
        self.base_url = "http://localhost:1234/v1"
        self.api_type = "open_ai"
        self.api_key = "not-needed"

# Function to initiate conversation with the local-model and establishes roles and where the instructions come from.
def initiate_conversation(input_text, system_message):
    response = openai.ChatCompletion.create(
        model="local-model",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": input_text}
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    system_message = "I'm Allen Sun. You are Aurora Nova. You are Allen's artificial intelligence assistant."
    model_response = initiate_conversation(user_input, system_message)
    return model_response

if __name__ == '__main__':
    # Instantiate configuration
    config = OpenAIConfig()
    openai.api_base = config.base_url
    openai.api_key = config.api_key

    app.run(debug=True)

