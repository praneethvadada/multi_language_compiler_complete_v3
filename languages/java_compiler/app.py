from flask import Flask, request, jsonify
import subprocess
import tempfile
import os
from concurrent.futures import ThreadPoolExecutor
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

executor = ThreadPoolExecutor(max_workers=500)

def run_test_case_java(code, input_data, expected_output):
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create temporary Java files
        java_file = os.path.join(temp_dir, "Main.java")
        with open(java_file, 'w') as f:
            f.write(code)

        try:
            # Compile the Java code
            compile_process = subprocess.run(
                ["javac", java_file],
                capture_output=True,
                text=True,
                timeout=5
            )

            if compile_process.returncode != 0:
                return {
                    "input": input_data,
                    "error": compile_process.stderr.strip(),
                    "success": False
                }

            # Execute the compiled Java program
            execute_process = subprocess.run(
                ["java", "-cp", temp_dir, "Main"],
                input=input_data,
                capture_output=True,
                text=True,
                timeout=5
            )

            actual_output = execute_process.stdout.strip()
            error_output = execute_process.stderr.strip()
            expected_output = expected_output.strip()

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

def run_program(language, code, testcases):
    if language.lower() != "java":
        return [{"error": "Unsupported language", "success": False}]

    futures = [executor.submit(run_test_case_java, code, tc['input'], tc['output']) for tc in testcases]
    results = [future.result() for future in futures]
    return results

@app.route('/compile', methods=['POST'])
def compile_batch():
    data = request.get_json()
    language = data.get('language')
    code = data.get('code')
    testcases = data.get('testcases')

    program_results = run_program(language, code, testcases)
    return jsonify(program_results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

# from flask import Flask, request, jsonify
# import subprocess
# import tempfile
# import os
# from concurrent.futures import ThreadPoolExecutor
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)

# executor = ThreadPoolExecutor(max_workers=500)

# def run_test_case_java(code, input_data, expected_output):
#     with tempfile.TemporaryDirectory() as temp_dir:
#         # Create temporary Java files
#         java_file = os.path.join(temp_dir, "Main.java")
#         with open(java_file, 'w') as f:
#             f.write(code)

#         try:
#             # Compile the Java code
#             compile_process = subprocess.run(
#                 ["javac", java_file],
#                 capture_output=True,
#                 text=True,
#                 timeout=5
#             )

#             if compile_process.returncode != 0:
#                 return {
#                     "input": input_data,
#                     "error": compile_process.stderr.strip(),
#                     "success": False
#                 }

#             # Execute the compiled Java program
#             execute_process = subprocess.run(
#                 ["java", "-cp", temp_dir, "Main"],
#                 input=input_data,
#                 capture_output=True,
#                 text=True,
#                 timeout=5
#             )

#             actual_output = execute_process.stdout.strip()
#             error_output = execute_process.stderr.strip()
#             expected_output = expected_output.strip()

#             return {
#                 "input": input_data,
#                 "expected_output": expected_output,
#                 "actual_output": actual_output,
#                 "error": error_output if error_output else None,
#                 "success": actual_output == expected_output
#             }

#         except subprocess.TimeoutExpired:
#             return {
#                 "input": input_data,
#                 "error": "Execution timed out",
#                 "success": False
#             }

# def run_program(language, code, testcases):
#     if language.lower() != "java":
#         return [{"error": "Unsupported language", "success": False}]

#     futures = [executor.submit(run_test_case_java, code, tc['input'], tc['output']) for tc in testcases]
#     results = [future.result() for future in futures]
#     return results

# @app.route('/compile', methods=['POST'])
# def compile_batch():
#     data = request.get_json()
#     language = data.get('language')
#     code = data.get('code')
#     testcases = data.get('testcases')

#     program_results = run_program(language, code, testcases)
#     return jsonify(program_results)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080)

# # import os
# # import subprocess
# # import uuid
# # from flask import Flask, jsonify, request
# # from flask_cors import CORS
# # import logging

# # app = Flask(__name__)
# # CORS(app)
# # logging.basicConfig(level=logging.DEBUG)


# # def compile_and_run_java(code, testcase):
# #     unique_id = uuid.uuid4()
# #     classname = f"Program_{unique_id}"
# #     filename = f"{classname}.java"

# #     # Replace the original class name with the unique classname
# #     if "public class Main" in code:
# #         code_with_unique_classname = code.replace("public class Main", f"public class {classname}")
# #     else:
# #         raise ValueError("Invalid Java code: Missing 'public class Main' declaration.")

# #     try:
# #         # Write the updated Java code to a file
# #         with open(filename, 'w') as f:
# #             f.write(code_with_unique_classname)

# #         # Compile the Java file
# #         compile_result = subprocess.run(['javac', filename], capture_output=True, text=True)
# #         if compile_result.returncode != 0:
# #             return {
# #                 'input': testcase['input'],
# #                 'error': f"Compilation failed: {compile_result.stderr}",
# #                 'success': False
# #             }

# #         # Execute the compiled program with the test case input
# #         process = subprocess.run(
# #             ['java', classname],
# #             input=testcase['input'],
# #             capture_output=True,
# #             text=True,
# #             timeout=5
# #         )

# #         actual_output = process.stdout.strip()
# #         expected_output = testcase['output'].strip()
# #         return {
# #             'input': testcase['input'],
# #             'expected_output': expected_output,
# #             'actual_output': actual_output,
# #             'success': actual_output == expected_output
# #         }

# #     except subprocess.TimeoutExpired:
# #         return {
# #             'input': testcase['input'],
# #             'error': "Execution timed out",
# #             'success': False
# #         }

# #     finally:
# #         # Clean up generated files
# #         if os.path.exists(f"{classname}.class"):
# #             os.remove(f"{classname}.class")
# #         if os.path.exists(filename):
# #             os.remove(filename)


# # @app.route('/execute', methods=['POST'])
# # # def execute_java_code():
# # #     logging.debug("Received request to /execute")
# # #     data = request.get_json()

# # #     if not data or 'language' not in data or 'code' not in data or 'testcases' not in data:
# # #         return jsonify({"error": "Invalid request format. Required keys: 'language', 'code', 'testcases'."}), 400

# # #     if data['language'] != "java":
# # #         return jsonify({"error": f"Unsupported language: {data['language']}. Only 'java' is supported."}), 400

# # #     code = data['code']
# # #     testcases = data['testcases']

# # #     results = []
# # #     for testcase in testcases:
# # #         try:
# # #             result = compile_and_run_java(code, testcase)
# # #             results.append(result)
# # #         except Exception as e:
# # #             logging.error(f"Error processing testcase: {str(e)}")
# # #             results.append({
# # #                 "input": testcase.get('input', ''),
# # #                 "error": f"Unexpected error occurred: {str(e)}",
# # #                 "success": False
# # #             })

# # #     return jsonify(results)

# # def compile_and_run_java(code, testcase):
# #     unique_id = uuid.uuid4()
# #     classname = f"Program_{unique_id}"
# #     filename = f"{classname}.java"

# #     # Replace the original class name with the unique classname
# #     if "public class Main{" in code:
# #         code_with_unique_classname = code.replace("public class Main{", f"public class {classname}{{")
# #     elif "public class Main " in code:
# #         code_with_unique_classname = code.replace("public class Main ", f"public class {classname} ")
# #     else:
# #         return {
# #             'input': testcase['input'],
# #             'error': "Invalid Java code: Missing 'public class Main' declaration.",
# #             'success': False
# #         }

# #     try:
# #         # Write the updated Java code to a file
# #         with open(filename, 'w') as f:
# #             f.write(code_with_unique_classname)

# #         # Compile the Java file
# #         compile_result = subprocess.run(['javac', filename], capture_output=True, text=True)
# #         if compile_result.returncode != 0:
# #             return {
# #                 'input': testcase['input'],
# #                 'error': f"Compilation failed: {compile_result.stderr}",
# #                 'success': False
# #             }

# #         # Execute the compiled program with the test case input
# #         process = subprocess.run(
# #             ['java', classname],
# #             input=testcase['input'],
# #             capture_output=True,
# #             text=True,
# #             timeout=5
# #         )

# #         actual_output = process.stdout.strip()
# #         expected_output = testcase['output'].strip()
# #         return {
# #             'input': testcase['input'],
# #             'expected_output': expected_output,
# #             'actual_output': actual_output,
# #             'success': actual_output == expected_output
# #         }

# #     except subprocess.TimeoutExpired:
# #         return {
# #             'input': testcase['input'],
# #             'error': "Execution timed out",
# #             'success': False
# #         }

# #     finally:
# #         # Clean up generated files
# #         if os.path.exists(f"{classname}.class"):
# #             os.remove(f"{classname}.class")
# #         if os.path.exists(filename):
# #             os.remove(filename)

# # @app.errorhandler(500)
# # def handle_internal_error(e):
# #     return jsonify({"error": "Internal server error", "details": str(e)}), 500


# # if __name__ == '__main__':
# #     app.run(host='0.0.0.0', port=8080)

# # # import os
# # # import subprocess
# # # import uuid
# # # from flask import Flask, jsonify, request
# # # from flask_cors import CORS

# # # app = Flask(__name__)
# # # CORS(app)

# # # @app.route('/execute', methods=['POST'])
# # # def compile_and_run_java(code, testcase):
# # #     # Generate a unique filename and classname
# # #     unique_id = uuid.uuid4()
# # #     classname = f"Program_{unique_id}"
# # #     filename = f"{classname}.java"

# # #     # Replace the original class name with the unique classname
# # #     if "public class Main" in code:
# # #         code_with_unique_classname = code.replace("public class Main", f"public class {classname}")
# # #     else:
# # #         return {
# # #             'input': testcase['input'],
# # #             'error': "Invalid Java code: Missing 'public class Main' declaration.",
# # #             'success': False
# # #         }

# # #     try:
# # #         # Write the updated Java code to a file
# # #         with open(filename, 'w') as f:
# # #             f.write(code_with_unique_classname)

# # #         # Compile the Java file
# # #         compile_result = subprocess.run(['javac', filename], capture_output=True, text=True)
# # #         if compile_result.returncode != 0:
# # #             return {
# # #                 'input': testcase['input'],
# # #                 'error': f"Compilation failed: {compile_result.stderr}",
# # #                 'success': False
# # #             }

# # #         # Execute the compiled program with the test case input
# # #         process = subprocess.run(
# # #             ['java', classname],
# # #             input=testcase['input'],
# # #             capture_output=True,
# # #             text=True,
# # #             timeout=5
# # #         )

# # #         # Compare the actual output with the expected output
# # #         actual_output = process.stdout.strip()
# # #         expected_output = testcase['output'].strip()
# # #         return {
# # #             'input': testcase['input'],
# # #             'expected_output': expected_output,
# # #             'actual_output': actual_output,
# # #             'success': actual_output == expected_output
# # #         }

# # #     except subprocess.TimeoutExpired:
# # #         return {
# # #             'input': testcase['input'],
# # #             'error': "Execution timed out",
# # #             'success': False
# # #         }

# # #     finally:
# # #         # Clean up generated files
# # #         if os.path.exists(f"{classname}.class"):
# # #             os.remove(f"{classname}.class")
# # #         if os.path.exists(filename):
# # #             os.remove(filename)


# # # # def execute_java_code():
# # # #     # Parse input JSON
# # # #     data = request.get_json()

# # # #     # Validate the required fields in the JSON
# # # #     if not data or 'language' not in data or 'code' not in data or 'testcases' not in data:
# # # #         return jsonify({"error": "Invalid request format. Required keys: 'language', 'code', 'testcases'."}), 400

# # # #     if data['language'] != "java":
# # # #         return jsonify({"error": f"Unsupported language: {data['language']}. Only 'java' is supported."}), 400

# # # #     code = data['code']
# # # #     testcases = data['testcases']

# # # #     # Generate a unique filename for the Java file
# # # #     unique_id = uuid.uuid4()
# # # #     filename = f"Program_{unique_id}.java"
# # # #     classname = f"Program_{unique_id}"

# # # #     # Replace the class name with the unique class name
# # # #     if "public class" in code:
# # # #         code_with_classname = code.replace("public class", f"public class {classname}")
# # # #     else:
# # # #         return jsonify({"error": "Invalid Java code: Missing 'public class' declaration."}), 400

# # # #     try:
# # # #         # Write the code to a file
# # # #         with open(filename, 'w') as f:
# # # #             f.write(code_with_classname)

# # # #         # Compile the Java code
# # # #         compile_result = subprocess.run(['javac', filename], capture_output=True, text=True)
# # # #         if compile_result.returncode != 0:
# # # #             return jsonify({"error": f"Compilation failed: {compile_result.stderr}"}), 400

# # # #         # Execute the compiled program for each test case
# # # #         results = []
# # # #         for testcase in testcases:
# # # #             input_data = testcase['input']
# # # #             expected_output = testcase['output']

# # # #             try:
# # # #                 process = subprocess.run(
# # # #                     ['java', classname],
# # # #                     input=input_data,
# # # #                     capture_output=True,
# # # #                     text=True,
# # # #                     timeout=5
# # # #                 )

# # # #                 actual_output = process.stdout.strip()
# # # #                 success = actual_output == expected_output

# # # #                 results.append({
# # # #                     "input": input_data,
# # # #                     "expected_output": expected_output,
# # # #                     "actual_output": actual_output,
# # # #                     "success": success
# # # #                 })

# # # #             except subprocess.TimeoutExpired:
# # # #                 results.append({
# # # #                     "input": input_data,
# # # #                     "error": "Execution timed out",
# # # #                     "success": False
# # # #                 })

# # # #     finally:
# # # #         # Clean up generated files
# # # #         if os.path.exists(f"{classname}.class"):
# # # #             os.remove(f"{classname}.class")
# # # #         if os.path.exists(filename):
# # # #             os.remove(filename)

# # # #     return jsonify(results)

# # # if __name__ == '__main__':
# # #     app.run(host='0.0.0.0', port=8080)

# # # # import uuid
# # # # import os
# # # # import subprocess
# # # # from concurrent.futures import ThreadPoolExecutor, as_completed
# # # # from flask import Flask, jsonify, request
# # # # from flask_cors import CORS

# # # # app = Flask(__name__)
# # # # CORS(app)  # Enables CORS for all routes

# # # # # Initialize the ThreadPoolExecutor with a maximum of 50 workers
# # # # executor = ThreadPoolExecutor(max_workers=50)

# # # # # def compile_and_run_java(code, testcase):
# # # # #     # Generate a unique filename for the Java file
# # # # #     unique_id = uuid.uuid4()
# # # # #     filename = f"Main_{unique_id}.java"
# # # # #     classname = f"Main_{unique_id}"

# # # # #     # Replace "public class Main" with the unique classname
# # # # #     code_with_unique_classname = code.replace("public class Main", f"public class {classname}")

# # # # #     # Write the Java code to the unique file
# # # # #     with open(filename, 'w') as f:
# # # # #         f.write(code_with_unique_classname)

# # # # #     # Compile the Java code
# # # # #     compile_result = subprocess.run(['javac', filename], capture_output=True, text=True)

# # # # #     if compile_result.returncode != 0:
# # # # #         # Compilation error
# # # # #         return {
# # # # #             'input': testcase['input'],
# # # # #             'error': compile_result.stderr,
# # # # #             'success': False
# # # # #         }

# # # # #     # Prepare to run the compiled Java program
# # # # #     try:
# # # # #         if "Scanner" in code:
# # # # #             # Handle cases where Java code uses System.in (Scanner)
# # # # #             process = subprocess.run(
# # # # #                 ['java', classname],
# # # # #                 input=testcase['input'],
# # # # #                 capture_output=True,
# # # # #                 text=True,
# # # # #                 timeout=5
# # # # #             )
# # # # #         else:
# # # # #             # Handle cases where Java code expects command-line arguments (args)
# # # # #             args = testcase['input'].split()
# # # # #             process = subprocess.run(
# # # # #                 ['java', classname] + args,
# # # # #                 capture_output=True,
# # # # #                 text=True,
# # # # #                 timeout=5
# # # # #             )

# # # # #         actual_output = process.stdout.strip()
# # # # #         expected_output = testcase['output'].strip()

# # # # #         return {
# # # # #             'input': testcase['input'],
# # # # #             'expected_output': expected_output,
# # # # #             'actual_output': actual_output,
# # # # #             'success': actual_output == expected_output
# # # # #         }

# # # # #     except subprocess.TimeoutExpired:
# # # # #         return {
# # # # #             'input': testcase['input'],
# # # # #             'error': 'Execution timed out',
# # # # #             'success': False
# # # # #         }
# # # # #     finally:
# # # # #         # Clean up compiled files and Java source file
# # # # #         if os.path.exists(f"{classname}.class"):
# # # # #             os.remove(f"{classname}.class")
# # # # #         if os.path.exists(filename):
# # # # #             os.remove(filename)








# # # # # def compile_and_run_java(code, testcase):
# # # # #     # Generate a unique filename for the Java file
# # # # #     unique_id = uuid.uuid4()
# # # # #     filename = f"Main_{unique_id}.java"
# # # # #     classname = f"Main_{unique_id}"

# # # # #     # Replace "public class Main" with the unique classname
# # # # #     if "public class Main" in code:
# # # # #         code_with_unique_classname = code.replace("public class Main", f"public class {classname}")
# # # # #     else:
# # # # #         first_line, *rest_of_code = code.splitlines()
# # # # #         code_with_unique_classname = f"public class {classname}\n" + "\n".join(rest_of_code)

# # # # #     # Write the Java code to the unique file
# # # # #     with open(filename, 'w') as f:
# # # # #         f.write(code_with_unique_classname)

# # # # #     # Compile the Java code
# # # # #     compile_result = subprocess.run(['javac', filename], capture_output=True, text=True)

# # # # #     if compile_result.returncode != 0:
# # # # #         # Compilation error
# # # # #         return {
# # # # #             'input': testcase['input'],
# # # # #             'error': f"Compilation failed for {filename}: {compile_result.stderr}",
# # # # #             'success': False
# # # # #         }

# # # # #     # Prepare to run the compiled Java program
# # # # #     try:
# # # # #         if "Scanner" in code:
# # # # #             # Handle cases where Java code uses System.in (Scanner)
# # # # #             process = subprocess.run(
# # # # #                 ['java', classname],
# # # # #                 input=testcase['input'],
# # # # #                 capture_output=True,
# # # # #                 text=True,
# # # # #                 timeout=5
# # # # #             )
# # # # #         else:
# # # # #             # Handle cases where Java code expects command-line arguments (args)
# # # # #             args = testcase['input'].split()
# # # # #             process = subprocess.run(
# # # # #                 ['java', classname] + args,
# # # # #                 capture_output=True,
# # # # #                 text=True,
# # # # #                 timeout=5
# # # # #             )

# # # # #         actual_output = process.stdout.strip()
# # # # #         expected_output = testcase['output'].strip()

# # # # #         return {
# # # # #             'input': testcase['input'],
# # # # #             'expected_output': expected_output,
# # # # #             'actual_output': actual_output,
# # # # #             'success': actual_output == expected_output
# # # # #         }

# # # # #     except subprocess.TimeoutExpired:
# # # # #         return {
# # # # #             'input': testcase['input'],
# # # # #             'error': 'Execution timed out',
# # # # #             'success': False
# # # # #         }
# # # # #     finally:
# # # # #         # Clean up compiled files and Java source file
# # # # #         if os.path.exists(f"{classname}.class"):
# # # # #             os.remove(f"{classname}.class")
# # # # #         if os.path.exists(filename):
# # # # #             os.remove(filename)















# # # # def compile_and_run_java(code, testcase):
# # # #     # Generate a unique filename for the Java file
# # # #     unique_id = uuid.uuid4()
# # # #     filename = f"Main_{unique_id}.java"
# # # #     classname = f"Main_{unique_id}"

# # # #     # Replace "public class Main" with the unique classname
# # # #     if "public class Main" in code:
# # # #         code_with_unique_classname = code.replace(
# # # #             "public class Main", f"public class {classname}"
# # # #         )
# # # #     else:
# # # #         return {
# # # #             'input': testcase['input'],
# # # #             'error': "Invalid Java code: 'public class Main' declaration not found.",
# # # #             'success': False
# # # #         }

# # # #     # Write the Java code to the unique file
# # # #     with open(filename, 'w') as f:
# # # #         f.write(code_with_unique_classname)

# # # #     # Compile the Java code
# # # #     compile_result = subprocess.run(['javac', filename], capture_output=True, text=True)

# # # #     if compile_result.returncode != 0:
# # # #         # Compilation error
# # # #         return {
# # # #             'input': testcase['input'],
# # # #             'error': f"Compilation failed for {filename}: {compile_result.stderr}",
# # # #             'success': False
# # # #         }

# # # #     # Prepare to run the compiled Java program
# # # #     try:
# # # #         if "Scanner" in code:
# # # #             # Handle cases where Java code uses System.in (Scanner)
# # # #             process = subprocess.run(
# # # #                 ['java', classname],
# # # #                 input=testcase['input'],
# # # #                 capture_output=True,
# # # #                 text=True,
# # # #                 timeout=5
# # # #             )
# # # #         else:
# # # #             # Handle cases where Java code expects command-line arguments (args)
# # # #             args = testcase['input'].split()
# # # #             process = subprocess.run(
# # # #                 ['java', classname] + args,
# # # #                 capture_output=True,
# # # #                 text=True,
# # # #                 timeout=5
# # # #             )

# # # #         actual_output = process.stdout.strip()
# # # #         expected_output = testcase['output'].strip()

# # # #         return {
# # # #             'input': testcase['input'],
# # # #             'expected_output': expected_output,
# # # #             'actual_output': actual_output,
# # # #             'success': actual_output == expected_output
# # # #         }

# # # #     except subprocess.TimeoutExpired:
# # # #         return {
# # # #             'input': testcase['input'],
# # # #             'error': 'Execution timed out',
# # # #             'success': False
# # # #         }
# # # #     finally:
# # # #         # Clean up compiled files and Java source file
# # # #         if os.path.exists(f"{classname}.class"):
# # # #             os.remove(f"{classname}.class")
# # # #         if os.path.exists(filename):
# # # #             os.remove(filename)






# # # # # @app.route('/compile', methods=['POST'])
# # # # # def compile_batch():
# # # # #     data = request.get_json()
# # # # #     programs = data.get('programs')
    
# # # # #     # Run each program concurrently
# # # # #     program_results = []
# # # # #     for prog in programs:
# # # # #         futures = [
# # # # #             executor.submit(compile_and_run_java, prog['code'], tc)
# # # # #             for tc in prog['testcases']
# # # # #         ]
# # # # #         program_results.append([future.result() for future in as_completed(futures)])

# # # # #     return jsonify(program_results)

# # # # # @app.route('/compile', methods=['POST'])
# # # # # def compile_batch():
# # # # #     data = request.get_json()
# # # # #     if not data or 'programs' not in data:
# # # # #         return jsonify({"error": "Invalid request format. 'programs' key is missing."}), 400
    
# # # # #     programs = data['programs']
# # # # #     program_results = []

# # # # #     for prog in programs:
# # # # #         futures = [
# # # # #             executor.submit(compile_and_run_java, prog['code'], tc)
# # # # #             for tc in prog['testcases']
# # # # #         ]
# # # # #         program_results.append([future.result() for future in as_completed(futures)])

# # # # #     return jsonify(program_results)

# # # # @app.route('/compile', methods=['POST'])
# # # # def compile_batch():
# # # #     data = request.get_json()

# # # #     if not data or 'language' not in data or 'code' not in data or 'testcases' not in data:
# # # #         return jsonify({"error": "Invalid request format. Required keys: 'language', 'code', 'testcases'."}), 400

# # # #     language = data['language']
# # # #     code = data['code']
# # # #     testcases = data['testcases']

# # # #     if language != "java":
# # # #         return jsonify({"error": f"Unsupported language: {language}. Only 'java' is supported."}), 400

# # # #     # Process the Java code with the test cases
# # # #     futures = [
# # # #         executor.submit(compile_and_run_java, code, testcase)
# # # #         for testcase in testcases
# # # #     ]
# # # #     results = [future.result() for future in as_completed(futures)]

# # # #     return jsonify(results)

# # # # if __name__ == '__main__':
# # # #     app.run(host='0.0.0.0', port=8080)

# # # # # import uuid
# # # # # import os
# # # # # import subprocess

# # # # # from flask import Flask, jsonify, request
# # # # # from flask_cors import CORS

# # # # # app = Flask(__name__)
# # # # # CORS(app)  # Enables CORS for all routes

# # # # # def compile_and_run_java(code, testcase):
# # # # #     # Generate a unique filename for the Java file
# # # # #     unique_id = uuid.uuid4()
# # # # #     filename = f"Main_{unique_id}.java"
# # # # #     classname = f"Main_{unique_id}"

# # # # #     # Replace "public class Main" with the unique classname
# # # # #     code_with_unique_classname = code.replace("public class Main", f"public class {classname}")

# # # # #     # Write the Java code to the unique file
# # # # #     with open(filename, 'w') as f:
# # # # #         f.write(code_with_unique_classname)

# # # # #     # Compile the Java code
# # # # #     compile_result = subprocess.run(['javac', filename], capture_output=True, text=True)

# # # # #     if compile_result.returncode != 0:
# # # # #         # Compilation error
# # # # #         return {
# # # # #             'input': testcase['input'],
# # # # #             'error': compile_result.stderr,
# # # # #             'success': False
# # # # #         }

# # # # #     # Prepare to run the compiled Java program
# # # # #     try:
# # # # #         if "Scanner" in code:
# # # # #             # Handle cases where Java code uses System.in (Scanner)
# # # # #             process = subprocess.run(
# # # # #                 ['java', classname],
# # # # #                 input=testcase['input'],
# # # # #                 capture_output=True,
# # # # #                 text=True,
# # # # #                 timeout=5
# # # # #             )
# # # # #         else:
# # # # #             # Handle cases where Java code expects command-line arguments (args)
# # # # #             args = testcase['input'].split()
# # # # #             process = subprocess.run(
# # # # #                 ['java', classname] + args,
# # # # #                 capture_output=True,
# # # # #                 text=True,
# # # # #                 timeout=5
# # # # #             )

# # # # #         actual_output = process.stdout.strip()
# # # # #         expected_output = testcase['output'].strip()

# # # # #         return {
# # # # #             'input': testcase['input'],
# # # # #             'expected_output': expected_output,
# # # # #             'actual_output': actual_output,
# # # # #             'success': actual_output == expected_output
# # # # #         }

# # # # #     except subprocess.TimeoutExpired:
# # # # #         return {
# # # # #             'input': testcase['input'],
# # # # #             'error': 'Execution timed out',
# # # # #             'success': False
# # # # #         }
# # # # #     finally:
# # # # #         # Clean up compiled files and Java source file
# # # # #         if os.path.exists(f"{classname}.class"):
# # # # #             os.remove(f"{classname}.class")
# # # # #         if os.path.exists(filename):
# # # # #             os.remove(filename)
# # # # # @app.route('/compile', methods=['POST'])
# # # # # def compile_batch():
# # # # #     data = request.get_json()
# # # # #     programs = data.get('programs')
    
# # # # #     # Run each program concurrently
# # # # #     program_results = []
# # # # #     for prog in programs:
# # # # #         futures = [
# # # # #             executor.submit(compile_and_run_java, prog['code'], tc)
# # # # #             for tc in prog['testcases']
# # # # #         ]
# # # # #         program_results.append([future.result() for future in as_completed(futures)])

# # # # #     return jsonify(program_results)

# # # # # if __name__ == '__main__':
# # # # #     app.run(host='0.0.0.0', port=8080)



# # # # # # def run_program(code, testcases):
# # # # # #     futures = [executor.submit(compile_and_run_java, code, tc) for tc in testcases]
# # # # # #     results = [future.result() for future in futures]
# # # # # #     return results

# # # # # # @app.route('/compile', methods=['POST'])
# # # # # # def compile_batch():
# # # # # #     data = request.get_json()
# # # # # #     programs = data.get('programs')

# # # # # #     program_futures = [executor.submit(run_program, prog['code'], prog['testcases']) for prog in programs]
# # # # # #     program_results = [future.result() for future in program_futures]

# # # # # #     return jsonify(program_results)

# # # # # # if __name__ == '__main__':
# # # # # #     app.run(host='0.0.0.0', port=8080)

# # # # # # from flask import Flask, request, jsonify
# # # # # # import subprocess
# # # # # # import os
# # # # # # from flask_cors import CORS
# # # # # # from concurrent.futures import ThreadPoolExecutor, as_completed
# # # # # # import tempfile

# # # # # # app = Flask(__name__)
# # # # # # CORS(app)

# # # # # # MAX_WORKERS = 50
# # # # # # executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)

# # # # # # # def compile_and_run_java(code, testcase):
# # # # # # #     with open('Main.java', 'w') as f:
# # # # # # #         f.write(code)
    
# # # # # # #     compile_result = subprocess.run(['javac', 'Main.java'], capture_output=True, text=True)
    
# # # # # # #     if compile_result.returncode != 0:
# # # # # # #         return {
# # # # # # #             'input': testcase['input'],
# # # # # # #             'error': compile_result.stderr,
# # # # # # #             'success': False
# # # # # # #         }

# # # # # # #     try:
# # # # # # #         process = subprocess.run(
# # # # # # #             ['java', 'Main'],
# # # # # # #             input=testcase['input'],  # Pass input directly from the test case
# # # # # # #             capture_output=True,
# # # # # # #             text=True,
# # # # # # #             timeout=5
# # # # # # #         )
# # # # # # #         actual_output = process.stdout.strip()
# # # # # # #         expected_output = testcase['output'].strip()
        
# # # # # # #         return {
# # # # # # #             'input': testcase['input'],
# # # # # # #             'expected_output': expected_output,
# # # # # # #             'actual_output': actual_output,
# # # # # # #             'success': actual_output == expected_output
# # # # # # #         }

# # # # # # #     except subprocess.TimeoutExpired:
# # # # # # #         return {
# # # # # # #             'input': testcase['input'],
# # # # # # #             'error': 'Execution timed out',
# # # # # # #             'success': False
# # # # # # #         }
# # # # # # #     finally:
# # # # # # #         if os.path.exists('Main.class'):
# # # # # # #             os.remove('Main.class')
# # # # # # #         if os.path.exists('Main.java'):
# # # # # # #             os.remove('Main.java')

# # # # # # def compile_and_run_java(code, testcase):
# # # # # #     with open('Main.java', 'w') as f:
# # # # # #         f.write(code)
    
# # # # # #     # Compile the Java code
# # # # # #     compile_result = subprocess.run(['javac', 'Main.java'], capture_output=True, text=True)
    
# # # # # #     if compile_result.returncode != 0:
# # # # # #         return {
# # # # # #             'input': testcase['input'],
# # # # # #             'error': compile_result.stderr,
# # # # # #             'success': False
# # # # # #         }

# # # # # #     try:
# # # # # #         if "Scanner" in code:
# # # # # #             # Handle cases where Java code uses System.in (Scanner)
# # # # # #             process = subprocess.run(
# # # # # #                 ['java', 'Main'],
# # # # # #                 input=testcase['input'],
# # # # # #                 capture_output=True,
# # # # # #                 text=True,
# # # # # #                 timeout=5
# # # # # #             )
# # # # # #         else:
# # # # # #             # Handle cases where Java code expects command-line arguments (args)
# # # # # #             args = testcase['input'].split()
# # # # # #             process = subprocess.run(
# # # # # #                 ['java', 'Main'] + args,
# # # # # #                 capture_output=True,
# # # # # #                 text=True,
# # # # # #                 timeout=5
# # # # # #             )

# # # # # #         actual_output = process.stdout.strip()
# # # # # #         expected_output = testcase['output'].strip()
        
# # # # # #         return {
# # # # # #             'input': testcase['input'],
# # # # # #             'expected_output': expected_output,
# # # # # #             'actual_output': actual_output,
# # # # # #             'success': actual_output == expected_output
# # # # # #         }

# # # # # #     except subprocess.TimeoutExpired:
# # # # # #         return {
# # # # # #             'input': testcase['input'],
# # # # # #             'error': 'Execution timed out',
# # # # # #             'success': False
# # # # # #         }
# # # # # #     finally:
# # # # # #         # Clean up compiled files
# # # # # #         if os.path.exists('Main.class'):
# # # # # #             os.remove('Main.class')
# # # # # #         if os.path.exists('Main.java'):
# # # # # #             os.remove('Main.java')



# # # # # # def run_program(code, testcases):
# # # # # #     futures = [executor.submit(compile_and_run_java, code, tc) for tc in testcases]
# # # # # #     results = [future.result() for future in futures]
# # # # # #     return results

# # # # # # @app.route('/compile', methods=['POST'])
# # # # # # def compile_batch():
# # # # # #     data = request.get_json()
# # # # # #     programs = data.get('programs')

# # # # # #     program_futures = [executor.submit(run_program, prog['code'], prog['testcases']) for prog in programs]
# # # # # #     program_results = [future.result() for future in program_futures]

# # # # # #     return jsonify(program_results)

# # # # # # if __name__ == '__main__':
# # # # # #     app.run(host='0.0.0.0', port=8080)


# # # # # # # from flask import Flask, request, jsonify
# # # # # # # import subprocess
# # # # # # # import os
# # # # # # # from flask_cors import CORS
# # # # # # # from concurrent.futures import ThreadPoolExecutor, as_completed

# # # # # # # app = Flask(__name__)
# # # # # # # CORS(app)

# # # # # # # # Define the number of maximum workers (threads) for concurrent processing
# # # # # # # executor = ThreadPoolExecutor(max_workers=50)

# # # # # # # def compile_and_run_java(code, testcase):
# # # # # # #     # Write the Java code to Main.java
# # # # # # #     with open('Main.java', 'w') as f:
# # # # # # #         f.write(code)
    
# # # # # # #     # Compile the Java code
# # # # # # #     compile_result = subprocess.run(['javac', 'Main.java'], capture_output=True, text=True)
    
# # # # # # #     if compile_result.returncode != 0:
# # # # # # #         return {
# # # # # # #             'input': testcase['input'],
# # # # # # #             'error': compile_result.stderr,
# # # # # # #             'success': False
# # # # # # #         }

# # # # # # #     # Run the compiled Java code with the input
# # # # # # #     try:
# # # # # # #         process = subprocess.run(
# # # # # # #             ['java', 'Main'], input=testcase['input'], capture_output=True, text=True, timeout=5
# # # # # # #         )
# # # # # # #         actual_output = process.stdout.strip()
# # # # # # #         expected_output = testcase['output'].strip()
        
# # # # # # #         return {
# # # # # # #             'input': testcase['input'],
# # # # # # #             'expected_output': expected_output,
# # # # # # #             'actual_output': actual_output,
# # # # # # #             'success': actual_output == expected_output
# # # # # # #         }

# # # # # # #     except subprocess.TimeoutExpired:
# # # # # # #         return {
# # # # # # #             'input': testcase['input'],
# # # # # # #             'error': 'Execution timed out',
# # # # # # #             'success': False
# # # # # # #         }
# # # # # # #     finally:
# # # # # # #         # Clean up compiled files
# # # # # # #         if os.path.exists('Main.class'):
# # # # # # #             os.remove('Main.class')
# # # # # # #         if os.path.exists('Main.java'):
# # # # # # #             os.remove('Main.java')

# # # # # # # @app.route('/compile', methods=['POST'])
# # # # # # # def compile_batch():
# # # # # # #     data = request.get_json()
# # # # # # #     programs = data.get('programs')

# # # # # # #     # Run each program concurrently
# # # # # # #     program_futures = [executor.submit(compile_and_run_java, prog['code'], prog['testcases']) for prog in programs]
# # # # # # #     program_results = [future.result() for future in program_futures]

# # # # # # #     return jsonify(program_results)

# # # # # # # if __name__ == '__main__':
# # # # # # #     app.run(host='0.0.0.0', port=8080)

# # # # # # # # from flask import Flask, request, jsonify
# # # # # # # # import subprocess
# # # # # # # # import os
# # # # # # # # from flask_cors import CORS
# # # # # # # # from concurrent.futures import ThreadPoolExecutor, as_completed

# # # # # # # # app = Flask(__name__)
# # # # # # # # CORS(app)  # Allow CORS for all routes

# # # # # # # # # Define the number of maximum workers (threads) for concurrent processing
# # # # # # # # MAX_WORKERS = 50

# # # # # # # # # Initialize the ThreadPoolExecutor with MAX_WORKERS
# # # # # # # # executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)

# # # # # # # # def compile_and_run_java(code, testcase):
# # # # # # # #     # Write the Java code to Main.java
# # # # # # # #     with open('Main.java', 'w') as f:
# # # # # # # #         f.write(code)
    
# # # # # # # #     # Compile the Java code
# # # # # # # #     compile_result = subprocess.run(['javac', 'Main.java'], capture_output=True, text=True)
    
# # # # # # # #     if compile_result.returncode != 0:
# # # # # # # #         return {
# # # # # # # #             'input': testcase['input'],
# # # # # # # #             'error': compile_result.stderr,
# # # # # # # #             'success': False
# # # # # # # #         }

# # # # # # # #     # Run the compiled Java code with the input
# # # # # # # #     try:
# # # # # # # #         process = subprocess.run(
# # # # # # # #             ['java', 'Main'], input=testcase['input'], capture_output=True, text=True, timeout=5
# # # # # # # #         )
# # # # # # # #         actual_output = process.stdout.strip()
# # # # # # # #         expected_output = testcase['output'].strip()
        
# # # # # # # #         return {
# # # # # # # #             'input': testcase['input'],
# # # # # # # #             'expected_output': expected_output,
# # # # # # # #             'actual_output': actual_output,
# # # # # # # #             'success': actual_output == expected_output
# # # # # # # #         }

# # # # # # # #     except subprocess.TimeoutExpired:
# # # # # # # #         return {
# # # # # # # #             'input': testcase['input'],
# # # # # # # #             'error': 'Execution timed out',
# # # # # # # #             'success': False
# # # # # # # #         }
# # # # # # # #     finally:
# # # # # # # #         # Clean up compiled files
# # # # # # # #         if os.path.exists('Main.class'):
# # # # # # # #             os.remove('Main.class')
# # # # # # # #         if os.path.exists('Main.java'):
# # # # # # # #             os.remove('Main.java')

# # # # # # # # @app.route('/compile', methods=['POST'])
# # # # # # # # def compile_code():
# # # # # # # #     data = request.get_json()
# # # # # # # #     code = data['code']
# # # # # # # #     testcases = data['testcases']

# # # # # # # #     # Run the code for each test case concurrently
# # # # # # # #     futures = [executor.submit(compile_and_run_java, code, testcase) for testcase in testcases]

# # # # # # # #     results = []
# # # # # # # #     for future in as_completed(futures):
# # # # # # # #         results.append(future.result())

# # # # # # # #     return jsonify(results)

# # # # # # # # if __name__ == '__main__':
# # # # # # # #     app.run(host='0.0.0.0', port=8080)

# # # # # # # # # from flask import Flask, request, jsonify
# # # # # # # # # import subprocess
# # # # # # # # # import os
# # # # # # # # # from flask_cors import CORS

# # # # # # # # # app = Flask(__name__)
# # # # # # # # # CORS(app)  # Allow CORS for all routes

# # # # # # # # # @app.route('/compile', methods=['POST'])
# # # # # # # # # def compile_code():
# # # # # # # # #     data = request.get_json()
# # # # # # # # #     code = data['code']
# # # # # # # # #     testcases = data['testcases']
    
# # # # # # # # #     # Write the Java code to Main.java
# # # # # # # # #     with open('Main.java', 'w') as f:
# # # # # # # # #         f.write(code)
    
# # # # # # # # #     # Compile the Java code
# # # # # # # # #     compile_result = subprocess.run(['javac', 'Main.java'], capture_output=True, text=True)
    
# # # # # # # # #     if compile_result.returncode != 0:
# # # # # # # # #         return jsonify({'error': compile_result.stderr}), 400

# # # # # # # # #     results = []
# # # # # # # # #     for testcase in testcases:
# # # # # # # # #         try:
# # # # # # # # #             process = subprocess.run(['java', 'Main'], input=testcase['input'], capture_output=True, text=True, timeout=5)
# # # # # # # # #             actual_output = process.stdout.strip()
# # # # # # # # #             expected_output = testcase['output'].strip()
            
# # # # # # # # #             results.append({
# # # # # # # # #                 'input': testcase['input'],
# # # # # # # # #                 'expected_output': expected_output,
# # # # # # # # #                 'actual_output': actual_output,
# # # # # # # # #                 'success': actual_output == expected_output
# # # # # # # # #             })

# # # # # # # # #         except subprocess.TimeoutExpired:
# # # # # # # # #             results.append({
# # # # # # # # #                 'input': testcase['input'],
# # # # # # # # #                 'error': 'Execution timed out',
# # # # # # # # #                 'success': False
# # # # # # # # #             })

# # # # # # # # #     # Clean up compiled files
# # # # # # # # #     if os.path.exists('Main.class'):
# # # # # # # # #         os.remove('Main.class')
# # # # # # # # #     if os.path.exists('Main.java'):
# # # # # # # # #         os.remove('Main.java')

# # # # # # # # #     return jsonify(results)

# # # # # # # # # if __name__ == '__main__':
# # # # # # # # #     app.run(host='0.0.0.0', port=8080)

