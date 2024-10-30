from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
CORS(app)  # Allow CORS for all routes

app = Flask(__name__)

# Map languages to their respective service URLs
LANGUAGE_URLS = {
    "python": "http://python_compiler:8080/compile",
    "java": "http://java_compiler:8080/compile",
    "csharp": "http://csharp_compiler:8080/compile",
    "cpp": "http://cpp_compiler:8080/compile",
    "c": "http://c_compiler:8080/compile"
}

@app.route('/run', methods=['POST'])
def run_code():
    data = request.json
    language = data.get('language')
    code = data.get('code')
    testcases = data.get('testcases')

    # Validate required fields
    if not language or not code or not testcases:
        return jsonify({"error": "Please provide language, code, and testcases"}), 400

    # Check if the language is supported
    if language not in LANGUAGE_URLS:
        return jsonify({"error": f"Language '{language}' not supported"}), 400

    # Forward request to the appropriate compiler service
    compiler_url = LANGUAGE_URLS[language]
    try:
        response = requests.post(compiler_url, json={"code": code, "testcases": testcases})
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to connect to the compiler service", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

# from flask import Flask, request, jsonify
# import requests

# app = Flask(__name__)

# # Define services for each language with their corresponding ports
# LANGUAGE_SERVICES = {
#     'python': 'http://python_compiler:8080/compile',
#     'cpp': 'http://cpp_compiler:8080/compile',
#     'c': 'http://c_compiler:8080/compile',
#     'java': 'http://java_compiler:8080/compile',
#     'csharp': 'http://csharp_compiler:8080/compile'
# }

# @app.route('/run', methods=['POST'])
# def route_request():
#     data = request.get_json()
#     language = data.get('language')
    
#     # Check if the specified language service exists
#     if language not in LANGUAGE_SERVICES:
#         return jsonify({'error': f'Language {language} not supported'}), 400
    
#     # Send request to the appropriate compiler service
#     try:
#         response = requests.post(LANGUAGE_SERVICES[language], json=data)
#         return jsonify(response.json()), response.status_code
#     except requests.exceptions.RequestException as e:
#         return jsonify({'error': 'Service unavailable', 'details': str(e)}), 503

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080)
