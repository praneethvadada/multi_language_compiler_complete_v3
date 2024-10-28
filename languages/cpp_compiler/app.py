from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/compile', methods=['POST'])
def compile_code():
    data = request.get_json()
    code = data.get('code')
    testcases = data.get('testcases', [])

    # Save the user's code to a file
    with open('main.cpp', 'w') as f:
        f.write(code)

    # Compile the C++ code
    compile_result = subprocess.run(['g++', 'main.cpp', '-o', 'main'], capture_output=True, text=True)
    
    if compile_result.returncode != 0:
        # Compilation error
        return jsonify({'error': compile_result.stderr}), 400

    # Run the compiled program for each testcase and capture the output
    results = []
    for testcase in testcases:
        input_data = testcase['input']
        
        # Run the compiled C++ program with the provided input
        try:
            process = subprocess.run(['./main'], input=input_data, capture_output=True, text=True, timeout=5)
            actual_output = process.stdout.strip()  # Strip to ensure exact match
            expected_output = testcase['output'].strip()  # Strip expected output

            # Append results preserving formatting
            results.append({
                'input': input_data,
                'expected_output': expected_output,
                'actual_output': actual_output,
                'success': actual_output == expected_output
            })
        
        except subprocess.TimeoutExpired:
            results.append({
                'input': input_data,
                'error': 'Execution timed out',
                'success': False
            })

    # Clean up the compiled binary and source file
    if os.path.exists('./main'):
        os.remove('./main')
    if os.path.exists('./main.cpp'):
        os.remove('./main.cpp')

    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

# from flask import Flask, request, jsonify
# import subprocess
# import os

# app = Flask(__name__)

# @app.route('/compile', methods=['POST'])
# def compile_code():
#     data = request.get_json()
#     code = data.get('code')
#     testcases = data.get('testcases', [])

#     # Save the user's code to a file
#     with open('main.cpp', 'w') as f:
#         f.write(code)

#     # Compile the C++ code
#     compile_result = subprocess.run(['g++', 'main.cpp', '-o', 'main'], capture_output=True, text=True)
    
#     if compile_result.returncode != 0:
#         # Compilation error
#         return jsonify({'error': compile_result.stderr}), 400

#     # Run the compiled program for each testcase and capture the output
#     results = []
#     for testcase in testcases:
#         input_data = testcase['input']
        
#         # Run the compiled C++ program with the provided input
#         try:
#             process = subprocess.run(['./main'], input=input_data, capture_output=True, text=True, timeout=5)
#             actual_output = process.stdout
            
#             # Append results preserving formatting
#             results.append({
#                 'input': input_data,
#                 'expected_output': testcase['output'],
#                 'actual_output': actual_output,
#                 'success': actual_output.strip() == testcase['output'].strip()
#             })
        
#         except subprocess.TimeoutExpired:
#             results.append({
#                 'input': input_data,
#                 'error': 'Execution timed out',
#                 'success': False
#             })

#     # Clean up the compiled binary
#     if os.path.exists('./main'):
#         os.remove('./main')
#     if os.path.exists('./main.cpp'):
#         os.remove('./main.cpp')

#     return jsonify(results)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080)

# # from flask import Flask, request, jsonify
# # import subprocess

# # app = Flask(__name__)

# # @app.route('/compile', methods=['POST'])
# # def compile_code():
# #     data = request.get_json()
# #     code = data['code']
# #     testcases = data['testcases']
    
# #     with open('main.cpp', 'w') as f:
# #         f.write(code)
    
# #     compile_result = subprocess.run(['g++', 'main.cpp', '-o', 'main'], capture_output=True, text=True)
    
# #     if compile_result.returncode != 0:
# #         return jsonify({'error': compile_result.stderr}), 400

# #     results = []
# #     for testcase in testcases:
# #         process = subprocess.run(['./main'], input=testcase['input'], capture_output=True, text=True)
# #         results.append({
# #             'input': testcase['input'],
# #             'expected_output': testcase['output'],
# #             'actual_output': process.stdout.strip(),
# #             'success': process.stdout.strip() == testcase['output']
# #         })

# #     return jsonify(results)

# # if __name__ == '__main__':
# #     app.run(host='0.0.0.0', port=8080)
