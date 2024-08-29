from flask import Blueprint, request, jsonify
from app.main.services import get_response

main_bp = Blueprint('main', __name__)

@main_bp.route('/api/get-response', methods=['POST'])
def api_get_response():
    data = request.json
    user_input = data.get('user_input', '')
    
    if not user_input:
        return jsonify({"error": "No user input provided"}), 400
    
    response_text = get_response(user_input)
    return jsonify({"response": response_text})
