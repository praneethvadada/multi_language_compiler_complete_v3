from flask import Flask, request, jsonify
import subprocess
import tempfile
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enables CORS for all routes

@app.route('/compile', methods=['POST'])
def compile_code():
    data = request.get_json()
    code = data.get('code')
    testcases = data.get('testcases')

    results = []
    for testcase in testcases:
        input_data = testcase['input']
        expected_output = testcase['output']
        
        # Create a temporary file for the Python code
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as temp_code_file:
            temp_code_file.write(code.encode())
            temp_code_file_name = temp_code_file.name

        # Run the Python code with the input, capturing stdout and stderr
        try:
            process = subprocess.run(
                ["python3", temp_code_file_name],
                input=input_data,  # Pass input directly without encoding
                capture_output=True,
                text=True,
                timeout=5
            )
            
            actual_output = process.stdout.strip()
            error_output = process.stderr.strip()  # Capture error output

            # Determine if the test case passed
            success = (actual_output == expected_output) and (process.returncode == 0)

            # Append the result, including error output if there's any
            results.append({
                "input": input_data,
                "expected_output": expected_output,
                "actual_output": actual_output,
                "error": error_output if error_output else None,  # Add error output if present
                "success": success
            })

        except subprocess.TimeoutExpired:
            results.append({
                "input": input_data,
                "error": "Execution timed out",
                "success": False
            })

    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)


# from flask import Flask, request, jsonify
# import subprocess
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)  # Enables CORS for all routes

# @app.route('/compile', methods=['POST'])
# def compile_code():
#     data = request.get_json()
#     code = data['code']
#     testcases = data['testcases']

#     results = []
#     for testcase in testcases:
#         # Run the code and capture output
#         process = subprocess.run(['python3', '-c', code], input=testcase['input'], capture_output=True, text=True)
        
#         # Normalize both expected and actual output by stripping any trailing whitespace
#         expected_output = testcase['output'].strip()
#         actual_output = process.stdout.strip()
        
#         results.append({
#             'input': testcase['input'],
#             'expected_output': expected_output,
#             'actual_output': actual_output,
#             'success': actual_output == expected_output
#         })

#     return jsonify(results)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080)
