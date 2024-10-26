from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/compile', methods=['POST'])
def compile_code():
    data = request.get_json()
    code = data.get('code')
    testcases = data.get('testcases')

    # Save code to a .cs file
    with open('/app/Program.cs', 'w') as f:
        f.write(code)

    # Compile the C# code
    compile_process = subprocess.run(
        ["csc", "/app/Program.cs", "-out:/app/Program.exe"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    if compile_process.returncode != 0:
        return jsonify({"error": compile_process.stderr.decode()}), 400

    # Run the compiled executable for each testcase
    results = []
    for testcase in testcases:
        input_data = testcase['input']
        expected_output = testcase['output']

        # Run the executable and pass the input
        run_process = subprocess.run(
            ["mono", "/app/Program.exe"], input=input_data.encode(),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        actual_output = run_process.stdout.decode().strip()
        results.append({
            "input": input_data,
            "expected_output": expected_output,
            "actual_output": actual_output,
            "passed": actual_output == expected_output
        })

    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

# from flask import Flask, request, jsonify
# import subprocess

# app = Flask(__name__)

# @app.route('/compile', methods=['POST'])
# def compile_code():
#     data = request.get_json()
#     code = data['code']
#     testcases = data['testcases']
    
#     with open('Program.cs', 'w') as f:
#         f.write(code)
    
#     compile_result = subprocess.run(['dotnet', 'run', 'Program.cs'], capture_output=True, text=True)
    
#     if compile_result.returncode != 0:
#         return jsonify({'error': compile_result.stderr}), 400

#     results = []
#     for testcase in testcases:
#         process = subprocess.run(['dotnet', 'run'], input=testcase['input'], capture_output=True, text=True)
#         results.append({
#             'input': testcase['input'],
#             'expected_output': testcase['output'],
#             'actual_output': process.stdout.strip(),
#             'success': process.stdout.strip() == testcase['output']
#         })

#     return jsonify(results)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080)
