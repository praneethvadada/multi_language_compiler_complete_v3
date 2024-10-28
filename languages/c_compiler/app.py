from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/compile', methods=['POST'])
def compile_code():
    data = request.get_json()
    code = data['code']
    testcases = data['testcases']
    
    with open('main.c', 'w') as f:
        f.write(code)
    
    compile_result = subprocess.run(['gcc', 'main.c', '-o', 'main'], capture_output=True, text=True)
    
    if compile_result.returncode != 0:
        return jsonify({'error': compile_result.stderr}), 400

    results = []
    for testcase in testcases:
        process = subprocess.run(['./main'], input=testcase['input'], capture_output=True, text=True)
        
        # Capture and strip outputs for an exact match
        actual_output = process.stdout.strip()
        expected_output = testcase['output'].strip()
        
        results.append({
            'input': testcase['input'],
            'expected_output': expected_output,
            'actual_output': actual_output,
            'success': actual_output == expected_output
        })

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

#     # Write the code to main.c file
#     with open('main.c', 'w') as f:
#         f.write(code)

#     # Compile the code
#     compile_result = subprocess.run(['gcc', 'main.c', '-o', 'main'], capture_output=True, text=True)

#     if compile_result.returncode != 0:
#         # Compilation error
#         return jsonify({'error': compile_result.stderr}), 400

#     # Run each test case and capture results
#     results = []
#     for testcase in testcases:
#         try:
#             process = subprocess.run(
#                 ['./main'],
#                 input=testcase['input'],
#                 capture_output=True,
#                 text=True,
#                 timeout=5  # Add a timeout to prevent infinite loops
#             )
#             # Strip the actual output to ensure it matches expected output formatting exactly
#             actual_output = process.stdout.strip()

#             # Append result to results list with preserved line breaks and formatting
#             results.append({
#                 'input': testcase['input'],
#                 'expected_output': testcase['output'],
#                 'actual_output': actual_output,
#                 'success': actual_output == testcase['output']
#             })
#         except subprocess.TimeoutExpired:
#             results.append({
#                 'input': testcase['input'],
#                 'expected_output': testcase['output'],
#                 'actual_output': '',
#                 'success': False,
#                 'error': 'Execution timed out'
#             })

#     # Clean up compiled file after execution
#     if os.path.exists('./main'):
#         os.remove('./main')

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
    
# #     with open('main.c', 'w') as f:
# #         f.write(code)
    
# #     compile_result = subprocess.run(['gcc', 'main.c', '-o', 'main'], capture_output=True, text=True)
    
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
