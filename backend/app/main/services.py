import requests
from app.config import Config

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
        "Authorization": f"Bearer {Config.API_KEY}"
    }

    try:
        response = requests.post(Config.API_URL, json=payload, headers=headers)
        response.raise_for_status()

        response_data = response.json()
        outputs = response_data.get('data', {}).get('outputs', [])
        if outputs:
            text = outputs[0].get('text', '')
            return text[:180] # This will reduce the output texts, you can remove it if you want.
        return 'I didn\'t get that.'

    except requests.exceptions.HTTPError as http_err:
        try:
            error_data = response.json()
            error_message = error_data.get('message', str(http_err))
        except ValueError:  
            error_message = str(http_err)
        return error_message
    except requests.exceptions.ConnectionError as conn_err:
        return f"Connection error occurred: {conn_err}"
    except requests.exceptions.Timeout as timeout_err:
        return f"Timeout error occurred: {timeout_err}"
    except requests.exceptions.RequestException as req_err:
        return f"An error occurred: {req_err}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"
