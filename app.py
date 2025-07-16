from flask import Flask, request, jsonify
from flask import send_from_directory
import requests

app = Flask(__name__)

API_URL = "https://jp957eyba6422ki8.us-east4.gcp.endpoints.huggingface.cloud"
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

@app.route('/api/query', methods=['POST'])
def handle_query():
    data = request.get_json()
    if not data or 'inputs' not in data:
        return jsonify({"error": "Missing 'inputs' in request"}), 400
    
    payload = {
        "inputs": data["inputs"],
        "parameters": {
            "max_new_tokens": data.get("max_new_tokens", 150)
        }
    }

    result = query(payload)
    return jsonify(result)

@app.route('/')
def home():
    return "Hugging Face API Gateway is running!"

@app.route('/ui')
def ui():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
