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
    
    # Write the Java code to Main.java
    with open('Main.java', 'w') as f:
        f.write(code)
    
    # Compile the Java code
    compile_result = subprocess.run(['javac', 'Main.java'], capture_output=True, text=True)
    
    if compile_result.returncode != 0:
        return jsonify({'error': compile_result.stderr}), 400

    results = []
    for testcase in testcases:
        try:
            process = subprocess.run(['java', 'Main'], input=testcase['input'], capture_output=True, text=True, timeout=5)
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

    # Clean up compiled files
    if os.path.exists('Main.class'):
        os.remove('Main.class')
    if os.path.exists('Main.java'):
        os.remove('Main.java')

    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)



# from flask import Flask, request, jsonify
# import subprocess
# import os
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)  # Allow CORS for all routes

# @app.route('/compile', methods=['POST'])
# def compile_code():
#     data = request.get_json()
#     code = data['code']
#     testcases = data['testcases']
    
#     with open('Main.java', 'w') as f:
#         f.write(code)
    
#     compile_result = subprocess.run(['javac', 'Main.java'], capture_output=True, text=True)
    
#     if compile_result.returncode != 0:
#         return jsonify({'error': compile_result.stderr}), 400

#     results = []
#     for testcase in testcases:
#         try:
#             process = subprocess.run(['java', 'Main'], input=testcase['input'], capture_output=True, text=True, timeout=5)
#             actual_output = process.stdout.strip()
#             expected_output = testcase['output'].strip()
            
#             results.append({
#                 'input': testcase['input'],
#                 'expected_output': expected_output,
#                 'actual_output': actual_output,
#                 'success': actual_output == expected_output
#             })

#         except subprocess.TimeoutExpired:
#             results.append({
#                 'input': testcase['input'],
#                 'error': 'Execution timed out',
#                 'success': False
#             })

#     # Clean up compiled files
#     if os.path.exists('Main.class'):
#         os.remove('Main.class')
#     if os.path.exists('Main.java'):
#         os.remove('Main.java')

#     return jsonify(results)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080)


