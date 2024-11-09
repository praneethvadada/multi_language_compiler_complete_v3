from flask import Flask, request, jsonify
import subprocess
import tempfile
import os
from concurrent.futures import ThreadPoolExecutor
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enables CORS for all routes

# Initialize ThreadPoolExecutor with a max of 500 workers
executor = ThreadPoolExecutor(max_workers=500)

def run_test_case(code, input_data, expected_output):
    # Create a temporary file for the Python code
    with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as temp_code_file:
        temp_code_file.write(code.encode())
        temp_code_file_name = temp_code_file.name

    try:
        # Run the Python code with the input, capturing stdout and stderr
        process = subprocess.run(
            ["python3", temp_code_file_name],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=5
        )
        
        actual_output = process.stdout.strip()  # Remove extra newlines and whitespace
        expected_output = expected_output.strip()  # Remove extra newlines and whitespace
        error_output = process.stderr.strip()

        return {
            "input": input_data,
            "expected_output": expected_output,
            "actual_output": actual_output,
            "error": error_output if error_output else None,
            "success": actual_output == expected_output
        }

    except subprocess.TimeoutExpired:
        return {
            "input": input_data,
            "error": "Execution timed out",
            "success": False
        }

    finally:
        # Clean up the temporary file after execution
        if os.path.exists(temp_code_file_name):
            os.remove(temp_code_file_name)

def run_program(language, code, testcases):
    # Ensure the language is supported
    if language.lower() != "python":
        return [{"error": "Unsupported language", "success": False}]

    # Run each test case for the given code in parallel
    futures = [executor.submit(run_test_case, code, tc['input'], tc['output']) for tc in testcases]
    results = [future.result() for future in futures]
    return results

@app.route('/compile', methods=['POST'])
def compile_batch():
    data = request.get_json()
    language = data.get('language')
    code = data.get('code')
    testcases = data.get('testcases')

    # Run the program and gather results
    program_results = run_program(language, code, testcases)

    return jsonify(program_results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)


# # from flask import Flask, request, jsonify
# # import subprocess
# # import tempfile
# # from concurrent.futures import ThreadPoolExecutor
# # from flask_cors import CORS

# # app = Flask(__name__)
# # CORS(app)  # Enables CORS for all routes

# # # Initialize ThreadPoolExecutor with a max of 50 workers
# # executor = ThreadPoolExecutor(max_workers=500)

# # def run_test_case(code, input_data, expected_output):
# #     # Create a temporary file for the Python code
# #     with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as temp_code_file:
# #         temp_code_file.write(code.encode())
# #         temp_code_file_name = temp_code_file.name

# #     # Run the Python code with the input, capturing stdout and stderr
# #     try:
# #         process = subprocess.run(
# #             ["python3", temp_code_file_name],
# #             input=input_data,
# #             capture_output=True,
# #             text=True,
# #             timeout=5
# #         )
        
# #         actual_output = process.stdout.strip()
# #         error_output = process.stderr.strip()

# #         return {
# #             "input": input_data,
# #             "expected_output": expected_output,
# #             "actual_output": actual_output,
# #             "error": error_output if error_output else None,
# #             "success": actual_output == expected_output
# #         }

# #     except subprocess.TimeoutExpired:
# #         return {
# #             "input": input_data,
# #             "error": "Execution timed out",
# #             "success": False
# #         }

# # def run_program(code, testcases):
# #     # Run each test case for the given code in parallel
# #     futures = [executor.submit(run_test_case, code, tc['input'], tc['output']) for tc in testcases]
# #     results = [future.result() for future in futures]
# #     return results

# # @app.route('/compile', methods=['POST'])
# # def compile_batch():
# #     data = request.get_json()
# #     programs = data.get('programs')

# #     # Run each program concurrently
# #     program_futures = [executor.submit(run_program, prog['code'], prog['testcases']) for prog in programs]
# #     program_results = [future.result() for future in program_futures]

# #     return jsonify(program_results)

# # if __name__ == '__main__':
# #     app.run(host='0.0.0.0', port=8080)





# from flask import Flask, request, jsonify
# import subprocess
# import tempfile
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)  # Enables CORS for all routes

# @app.route('/compile', methods=['POST'])
# def compile_code():
#     data = request.get_json()
#     code = data.get('code')
#     testcases = data.get('testcases')

#     results = []
#     for testcase in testcases:
#         input_data = testcase['input']
#         expected_output = testcase['output']
        
#         # Create a temporary file for the Python code
#         with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as temp_code_file:
#             temp_code_file.write(code.encode())
#             temp_code_file_name = temp_code_file.name

#         # Run the Python code with the input, capturing stdout and stderr
#         try:
#             process = subprocess.run(
#                 ["python3", temp_code_file_name],
#                 input=input_data,  # Pass input directly without encoding
#                 capture_output=True,
#                 text=True,
#                 timeout=5
#             )
            
#             actual_output = process.stdout.strip()
#             error_output = process.stderr.strip()  # Capture error output

#             # Determine if the test case passed
#             success = (actual_output == expected_output) and (process.returncode == 0)

#             # Append the result, including error output if there's any
#             results.append({
#                 "input": input_data,
#                 "expected_output": expected_output,
#                 "actual_output": actual_output,
#                 "error": error_output if error_output else None,  # Add error output if present
#                 "success": success
#             })

#         except subprocess.TimeoutExpired:
#             results.append({
#                 "input": input_data,
#                 "error": "Execution timed out",
#                 "success": False
#             })

#     return jsonify(results)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080)
