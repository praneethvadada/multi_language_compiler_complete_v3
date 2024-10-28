# from flask import Flask, request, jsonify
# import subprocess
# import tempfile
# import os

# app = Flask(__name__)

# @app.route('/run', methods=['POST'])
# def run_code():
#     data = request.get_json()
#     code = data.get('code')
#     testcases = data.get('testcases')

#     results = []
#     for testcase in testcases:
#         input_data = testcase['input']
#         expected_output = testcase['output'].strip()

#         # Create a temporary file for the Python code
#         with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as temp_code_file:
#             temp_code_file.write(code.encode())
#             temp_code_file_name = temp_code_file.name

#         # Run the Python code with the input
#         try:
#             process = subprocess.run(
#                 ["python3", temp_code_file_name],
#                 input=input_data.encode(),
#                 capture_output=True,
#                 text=True,
#                 timeout=5
#             )

#             actual_output = process.stdout.strip()
#             success = actual_output == expected_output
#             results.append({
#                 "input": input_data,
#                 "expected_output": expected_output,
#                 "actual_output": actual_output,
#                 "success": success
#             })

#         except subprocess.TimeoutExpired:
#             results.append({
#                 'input': input_data,
#                 'error': 'Execution timed out',
#                 'success': False
#             })
        
#         finally:
#             # Clean up temporary file
#             os.remove(temp_code_file_name)

#     return jsonify(results)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080)

# # from flask import Flask, request, jsonify
# # import subprocess
# # import tempfile

# # app = Flask(__name__)

# # @app.route('/run', methods=['POST'])
# # def run_code():
# #     data = request.get_json()
# #     code = data.get('code')
# #     testcases = data.get('testcases')

# #     results = []
# #     for testcase in testcases:
# #         input_data = testcase['input']
# #         expected_output = testcase['output']
        
# #         # Create a temporary file for the Python code
# #         with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as temp_code_file:
# #             temp_code_file.write(code.encode())
# #             temp_code_file_name = temp_code_file.name

# #         # Run the Python code with the input
# #         process = subprocess.run(
# #             ["python3", temp_code_file_name],
# #             input=input_data.encode(),
# #             capture_output=True,
# #             text=True
# #         )

# #         # Collect results
# #         actual_output = process.stdout.strip()
# #         success = actual_output == expected_output
# #         results.append({
# #             "input": input_data,
# #             "expected_output": expected_output,
# #             "actual_output": actual_output,
# #             "success": success
# #         })

# #     return jsonify(results)

# # if __name__ == '__main__':
# #     app.run(host='0.0.0.0', port=8080)


# from flask import Flask, request, jsonify
# import subprocess

# app = Flask(__name__)

# @app.route('/compile', methods=['POST'])
# def compile_code():
#     data = request.get_json()
#     code = data['code']
#     testcases = data['testcases']

#     results = []
#     for testcase in testcases:
#         process = subprocess.run(['python3', '-c', code], input=testcase['input'], capture_output=True, text=True)
#         results.append({
#             'input': testcase['input'],
#             'expected_output': testcase['output'],
#             'actual_output': process.stdout.strip(),
#             'success': process.stdout.strip() == testcase['output']
#         })

#     return jsonify(results)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080)

from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/compile', methods=['POST'])
def compile_code():
    data = request.get_json()
    code = data['code']
    testcases = data['testcases']

    results = []
    for testcase in testcases:
        # Run the code and capture output
        process = subprocess.run(['python3', '-c', code], input=testcase['input'], capture_output=True, text=True)
        
        # Normalize both expected and actual output by stripping any trailing whitespace
        expected_output = testcase['output'].strip()
        actual_output = process.stdout.strip()
        
        results.append({
            'input': testcase['input'],
            'expected_output': expected_output,
            'actual_output': actual_output,
            'success': actual_output == expected_output
        })

    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
