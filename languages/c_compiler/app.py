from flask import Flask, request, jsonify
import subprocess
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow CORS for all routes

@app.route('/compile', methods=['POST'])
def compile_code():
    data = request.get_json()
    code = data['code']
    testcases = data['testcases']
    
    # Write the C code to main.c
    with open('main.c', 'w') as f:
        f.write(code)
    
    # Compile the C code
    compile_result = subprocess.run(['gcc', 'main.c', '-o', 'main'], capture_output=True, text=True)
    
    if compile_result.returncode != 0:
        return jsonify({'error': compile_result.stderr}), 400

    results = []
    for testcase in testcases:
        try:
            process = subprocess.run(['./main'], input=testcase['input'], capture_output=True, text=True, timeout=5)
            actual_output = process.stdout.strip()
            expected_output = testcase['output'].strip()
            
            results.append({
                'input': testcase['input'],
                'expected_output': expected_output,
                'actual_output': actual_output,
                'success': actual_output == expected_output
            })
        
        except subprocess.TimeoutExpired:
            results.append({
                'input': testcase['input'],
                'error': 'Execution timed out',
                'success': False
            })

    # Clean up compiled binary and source files
    if os.path.exists('main'):
        os.remove('main')
    if os.path.exists('main.c'):
        os.remove('main.c')

    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

# from flask import Flask, request, jsonify
# import subprocess
# from flask_cors import CORS
# app = Flask(__name__)
# CORS(app)  # Allow CORS for all routes

# @app.route('/compile', methods=['POST'])
# def compile_code():
#     data = request.get_json()
#     code = data['code']
#     testcases = data['testcases']
    
#     with open('main.c', 'w') as f:
#         f.write(code)
    
#     compile_result = subprocess.run(['gcc', 'main.c', '-o', 'main'], capture_output=True, text=True)
    
#     if compile_result.returncode != 0:
#         return jsonify({'error': compile_result.stderr}), 400

#     results = []
#     for testcase in testcases:
#         process = subprocess.run(['./main'], input=testcase['input'], capture_output=True, text=True)
        
#         # Capture and strip outputs for an exact match
#         actual_output = process.stdout.strip()
#         expected_output = testcase['output'].strip()
        
#         results.append({
#             'input': testcase['input'],
#             'expected_output': expected_output,
#             'actual_output': actual_output,
#             'success': actual_output == expected_output
#         })

#     return jsonify(results)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080)
