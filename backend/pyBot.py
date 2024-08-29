from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

API_KEY = 'your_api_key' #From > https://textcortex.com/text-generation-api
API_URL =  'https://api.textcortex.com/v1/texts/completions'

def get_response(user_input):
    payload = {
        "formality": "default",
        "max_tokens": 2048,
        "model": "claude-3-haiku",
        "n": 1,
        "source_lang": "en",
        "target_lang": "en",
        "temperature": 0.7,
        "text": user_input
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()

        response_data = response.json()
        outputs = response_data.get('data', {}).get('outputs', [])
        if outputs:
            text = outputs[0].get('text', '')
            return text[:180] #This will reduce the output texts, you can remove it if you want.
        return 'I didn\'t get that.'

    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}. Response content: {response.text}"
    except requests.exceptions.ConnectionError as conn_err:
        return f"Connection error occurred: {conn_err}"
    except requests.exceptions.Timeout as timeout_err:
        return f"Timeout error occurred: {timeout_err}"
    except requests.exceptions.RequestException as req_err:
        return f"An error occurred: {req_err}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

@app.route('/api/get-response', methods=['POST'])
def api_get_response():
    data = request.json
    user_input = data.get('user_input', '')
    
    if not user_input:
        return jsonify({"error": "No user input provided"}), 400
    
    response_text = get_response(user_input)
    return jsonify({"response": response_text})

if __name__ == '__main__':
    app.run(debug=True)