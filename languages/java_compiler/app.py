import uuid
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enables CORS for all routes

# Initialize the ThreadPoolExecutor with a maximum of 50 workers
executor = ThreadPoolExecutor(max_workers=50)

def compile_and_run_java(code, testcase):
    # Generate a unique filename for the Java file
    unique_id = uuid.uuid4()
    filename = f"Main_{unique_id}.java"
    classname = f"Main_{unique_id}"

    # Replace "public class Main" with the unique classname
    code_with_unique_classname = code.replace("public class Main", f"public class {classname}")

    # Write the Java code to the unique file
    with open(filename, 'w') as f:
        f.write(code_with_unique_classname)

    # Compile the Java code
    compile_result = subprocess.run(['javac', filename], capture_output=True, text=True)

    if compile_result.returncode != 0:
        # Compilation error
        return {
            'input': testcase['input'],
            'error': compile_result.stderr,
            'success': False
        }

    # Prepare to run the compiled Java program
    try:
        if "Scanner" in code:
            # Handle cases where Java code uses System.in (Scanner)
            process = subprocess.run(
                ['java', classname],
                input=testcase['input'],
                capture_output=True,
                text=True,
                timeout=5
            )
        else:
            # Handle cases where Java code expects command-line arguments (args)
            args = testcase['input'].split()
            process = subprocess.run(
                ['java', classname] + args,
                capture_output=True,
                text=True,
                timeout=5
            )

        actual_output = process.stdout.strip()
        expected_output = testcase['output'].strip()

        return {
            'input': testcase['input'],
            'expected_output': expected_output,
            'actual_output': actual_output,
            'success': actual_output == expected_output
        }

    except subprocess.TimeoutExpired:
        return {
            'input': testcase['input'],
            'error': 'Execution timed out',
            'success': False
        }
    finally:
        # Clean up compiled files and Java source file
        if os.path.exists(f"{classname}.class"):
            os.remove(f"{classname}.class")
        if os.path.exists(filename):
            os.remove(filename)

@app.route('/compile', methods=['POST'])
def compile_batch():
    data = request.get_json()
    programs = data.get('programs')
    
    # Run each program concurrently
    program_results = []
    for prog in programs:
        futures = [
            executor.submit(compile_and_run_java, prog['code'], tc)
            for tc in prog['testcases']
        ]
        program_results.append([future.result() for future in as_completed(futures)])

    return jsonify(program_results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

# import uuid
# import os
# import subprocess

# from flask import Flask, jsonify, request
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)  # Enables CORS for all routes

# def compile_and_run_java(code, testcase):
#     # Generate a unique filename for the Java file
#     unique_id = uuid.uuid4()
#     filename = f"Main_{unique_id}.java"
#     classname = f"Main_{unique_id}"

#     # Replace "public class Main" with the unique classname
#     code_with_unique_classname = code.replace("public class Main", f"public class {classname}")

#     # Write the Java code to the unique file
#     with open(filename, 'w') as f:
#         f.write(code_with_unique_classname)

#     # Compile the Java code
#     compile_result = subprocess.run(['javac', filename], capture_output=True, text=True)

#     if compile_result.returncode != 0:
#         # Compilation error
#         return {
#             'input': testcase['input'],
#             'error': compile_result.stderr,
#             'success': False
#         }

#     # Prepare to run the compiled Java program
#     try:
#         if "Scanner" in code:
#             # Handle cases where Java code uses System.in (Scanner)
#             process = subprocess.run(
#                 ['java', classname],
#                 input=testcase['input'],
#                 capture_output=True,
#                 text=True,
#                 timeout=5
#             )
#         else:
#             # Handle cases where Java code expects command-line arguments (args)
#             args = testcase['input'].split()
#             process = subprocess.run(
#                 ['java', classname] + args,
#                 capture_output=True,
#                 text=True,
#                 timeout=5
#             )

#         actual_output = process.stdout.strip()
#         expected_output = testcase['output'].strip()

#         return {
#             'input': testcase['input'],
#             'expected_output': expected_output,
#             'actual_output': actual_output,
#             'success': actual_output == expected_output
#         }

#     except subprocess.TimeoutExpired:
#         return {
#             'input': testcase['input'],
#             'error': 'Execution timed out',
#             'success': False
#         }
#     finally:
#         # Clean up compiled files and Java source file
#         if os.path.exists(f"{classname}.class"):
#             os.remove(f"{classname}.class")
#         if os.path.exists(filename):
#             os.remove(filename)
# @app.route('/compile', methods=['POST'])
# def compile_batch():
#     data = request.get_json()
#     programs = data.get('programs')
    
#     # Run each program concurrently
#     program_results = []
#     for prog in programs:
#         futures = [
#             executor.submit(compile_and_run_java, prog['code'], tc)
#             for tc in prog['testcases']
#         ]
#         program_results.append([future.result() for future in as_completed(futures)])

#     return jsonify(program_results)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080)



# # def run_program(code, testcases):
# #     futures = [executor.submit(compile_and_run_java, code, tc) for tc in testcases]
# #     results = [future.result() for future in futures]
# #     return results

# # @app.route('/compile', methods=['POST'])
# # def compile_batch():
# #     data = request.get_json()
# #     programs = data.get('programs')

# #     program_futures = [executor.submit(run_program, prog['code'], prog['testcases']) for prog in programs]
# #     program_results = [future.result() for future in program_futures]

# #     return jsonify(program_results)

# # if __name__ == '__main__':
# #     app.run(host='0.0.0.0', port=8080)

# # from flask import Flask, request, jsonify
# # import subprocess
# # import os
# # from flask_cors import CORS
# # from concurrent.futures import ThreadPoolExecutor, as_completed
# # import tempfile

# # app = Flask(__name__)
# # CORS(app)

# # MAX_WORKERS = 50
# # executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)

# # # def compile_and_run_java(code, testcase):
# # #     with open('Main.java', 'w') as f:
# # #         f.write(code)
    
# # #     compile_result = subprocess.run(['javac', 'Main.java'], capture_output=True, text=True)
    
# # #     if compile_result.returncode != 0:
# # #         return {
# # #             'input': testcase['input'],
# # #             'error': compile_result.stderr,
# # #             'success': False
# # #         }

# # #     try:
# # #         process = subprocess.run(
# # #             ['java', 'Main'],
# # #             input=testcase['input'],  # Pass input directly from the test case
# # #             capture_output=True,
# # #             text=True,
# # #             timeout=5
# # #         )
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
# # #             'error': 'Execution timed out',
# # #             'success': False
# # #         }
# # #     finally:
# # #         if os.path.exists('Main.class'):
# # #             os.remove('Main.class')
# # #         if os.path.exists('Main.java'):
# # #             os.remove('Main.java')

# # def compile_and_run_java(code, testcase):
# #     with open('Main.java', 'w') as f:
# #         f.write(code)
    
# #     # Compile the Java code
# #     compile_result = subprocess.run(['javac', 'Main.java'], capture_output=True, text=True)
    
# #     if compile_result.returncode != 0:
# #         return {
# #             'input': testcase['input'],
# #             'error': compile_result.stderr,
# #             'success': False
# #         }

# #     try:
# #         if "Scanner" in code:
# #             # Handle cases where Java code uses System.in (Scanner)
# #             process = subprocess.run(
# #                 ['java', 'Main'],
# #                 input=testcase['input'],
# #                 capture_output=True,
# #                 text=True,
# #                 timeout=5
# #             )
# #         else:
# #             # Handle cases where Java code expects command-line arguments (args)
# #             args = testcase['input'].split()
# #             process = subprocess.run(
# #                 ['java', 'Main'] + args,
# #                 capture_output=True,
# #                 text=True,
# #                 timeout=5
# #             )

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
# #             'error': 'Execution timed out',
# #             'success': False
# #         }
# #     finally:
# #         # Clean up compiled files
# #         if os.path.exists('Main.class'):
# #             os.remove('Main.class')
# #         if os.path.exists('Main.java'):
# #             os.remove('Main.java')



# # def run_program(code, testcases):
# #     futures = [executor.submit(compile_and_run_java, code, tc) for tc in testcases]
# #     results = [future.result() for future in futures]
# #     return results

# # @app.route('/compile', methods=['POST'])
# # def compile_batch():
# #     data = request.get_json()
# #     programs = data.get('programs')

# #     program_futures = [executor.submit(run_program, prog['code'], prog['testcases']) for prog in programs]
# #     program_results = [future.result() for future in program_futures]

# #     return jsonify(program_results)

# # if __name__ == '__main__':
# #     app.run(host='0.0.0.0', port=8080)


# # # from flask import Flask, request, jsonify
# # # import subprocess
# # # import os
# # # from flask_cors import CORS
# # # from concurrent.futures import ThreadPoolExecutor, as_completed

# # # app = Flask(__name__)
# # # CORS(app)

# # # # Define the number of maximum workers (threads) for concurrent processing
# # # executor = ThreadPoolExecutor(max_workers=50)

# # # def compile_and_run_java(code, testcase):
# # #     # Write the Java code to Main.java
# # #     with open('Main.java', 'w') as f:
# # #         f.write(code)
    
# # #     # Compile the Java code
# # #     compile_result = subprocess.run(['javac', 'Main.java'], capture_output=True, text=True)
    
# # #     if compile_result.returncode != 0:
# # #         return {
# # #             'input': testcase['input'],
# # #             'error': compile_result.stderr,
# # #             'success': False
# # #         }

# # #     # Run the compiled Java code with the input
# # #     try:
# # #         process = subprocess.run(
# # #             ['java', 'Main'], input=testcase['input'], capture_output=True, text=True, timeout=5
# # #         )
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
# # #             'error': 'Execution timed out',
# # #             'success': False
# # #         }
# # #     finally:
# # #         # Clean up compiled files
# # #         if os.path.exists('Main.class'):
# # #             os.remove('Main.class')
# # #         if os.path.exists('Main.java'):
# # #             os.remove('Main.java')

# # # @app.route('/compile', methods=['POST'])
# # # def compile_batch():
# # #     data = request.get_json()
# # #     programs = data.get('programs')

# # #     # Run each program concurrently
# # #     program_futures = [executor.submit(compile_and_run_java, prog['code'], prog['testcases']) for prog in programs]
# # #     program_results = [future.result() for future in program_futures]

# # #     return jsonify(program_results)

# # # if __name__ == '__main__':
# # #     app.run(host='0.0.0.0', port=8080)

# # # # from flask import Flask, request, jsonify
# # # # import subprocess
# # # # import os
# # # # from flask_cors import CORS
# # # # from concurrent.futures import ThreadPoolExecutor, as_completed

# # # # app = Flask(__name__)
# # # # CORS(app)  # Allow CORS for all routes

# # # # # Define the number of maximum workers (threads) for concurrent processing
# # # # MAX_WORKERS = 50

# # # # # Initialize the ThreadPoolExecutor with MAX_WORKERS
# # # # executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)

# # # # def compile_and_run_java(code, testcase):
# # # #     # Write the Java code to Main.java
# # # #     with open('Main.java', 'w') as f:
# # # #         f.write(code)
    
# # # #     # Compile the Java code
# # # #     compile_result = subprocess.run(['javac', 'Main.java'], capture_output=True, text=True)
    
# # # #     if compile_result.returncode != 0:
# # # #         return {
# # # #             'input': testcase['input'],
# # # #             'error': compile_result.stderr,
# # # #             'success': False
# # # #         }

# # # #     # Run the compiled Java code with the input
# # # #     try:
# # # #         process = subprocess.run(
# # # #             ['java', 'Main'], input=testcase['input'], capture_output=True, text=True, timeout=5
# # # #         )
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
# # # #         # Clean up compiled files
# # # #         if os.path.exists('Main.class'):
# # # #             os.remove('Main.class')
# # # #         if os.path.exists('Main.java'):
# # # #             os.remove('Main.java')

# # # # @app.route('/compile', methods=['POST'])
# # # # def compile_code():
# # # #     data = request.get_json()
# # # #     code = data['code']
# # # #     testcases = data['testcases']

# # # #     # Run the code for each test case concurrently
# # # #     futures = [executor.submit(compile_and_run_java, code, testcase) for testcase in testcases]

# # # #     results = []
# # # #     for future in as_completed(futures):
# # # #         results.append(future.result())

# # # #     return jsonify(results)

# # # # if __name__ == '__main__':
# # # #     app.run(host='0.0.0.0', port=8080)

# # # # # from flask import Flask, request, jsonify
# # # # # import subprocess
# # # # # import os
# # # # # from flask_cors import CORS

# # # # # app = Flask(__name__)
# # # # # CORS(app)  # Allow CORS for all routes

# # # # # @app.route('/compile', methods=['POST'])
# # # # # def compile_code():
# # # # #     data = request.get_json()
# # # # #     code = data['code']
# # # # #     testcases = data['testcases']
    
# # # # #     # Write the Java code to Main.java
# # # # #     with open('Main.java', 'w') as f:
# # # # #         f.write(code)
    
# # # # #     # Compile the Java code
# # # # #     compile_result = subprocess.run(['javac', 'Main.java'], capture_output=True, text=True)
    
# # # # #     if compile_result.returncode != 0:
# # # # #         return jsonify({'error': compile_result.stderr}), 400

# # # # #     results = []
# # # # #     for testcase in testcases:
# # # # #         try:
# # # # #             process = subprocess.run(['java', 'Main'], input=testcase['input'], capture_output=True, text=True, timeout=5)
# # # # #             actual_output = process.stdout.strip()
# # # # #             expected_output = testcase['output'].strip()
            
# # # # #             results.append({
# # # # #                 'input': testcase['input'],
# # # # #                 'expected_output': expected_output,
# # # # #                 'actual_output': actual_output,
# # # # #                 'success': actual_output == expected_output
# # # # #             })

# # # # #         except subprocess.TimeoutExpired:
# # # # #             results.append({
# # # # #                 'input': testcase['input'],
# # # # #                 'error': 'Execution timed out',
# # # # #                 'success': False
# # # # #             })

# # # # #     # Clean up compiled files
# # # # #     if os.path.exists('Main.class'):
# # # # #         os.remove('Main.class')
# # # # #     if os.path.exists('Main.java'):
# # # # #         os.remove('Main.java')

# # # # #     return jsonify(results)

# # # # # if __name__ == '__main__':
# # # # #     app.run(host='0.0.0.0', port=8080)

