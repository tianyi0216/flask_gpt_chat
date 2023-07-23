from flask import Flask, request, jsonify, Response
import openai
import datetime

app = Flask(__name__)

API_KEY = 'replace with your API key'
openai.api_key = API_KEY

model_id = 'gpt-4' # replace with your model ID

messages = []
messages.append({'role': 'system', 'content': 'How may I help you?'})

def ChatGPT_conversation(conversation):
    response = openai.ChatCompletion.create(
        model=model_id,
        messages=conversation
    )
    reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
    return reply

@app.route('/')
def home():
    with open("index.html") as f:
        html = f.read()
    return html

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    messages.append({'role': 'user', 'content': userText})
    return str(ChatGPT_conversation(messages))

@app.route('/save', methods=['POST'])
def save():
    current_time = datetime.datetime.now()
    time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
    file_name = 'history_' + time_str + '.txt'
    with open(file_name, 'w') as file:
        for message in messages:
            file.write(str(message) + '\n')
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, threaded=False) # don't change this line!