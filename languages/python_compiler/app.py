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
        process = subprocess.run(['python3', '-c', code], input=testcase['input'], capture_output=True, text=True)
        results.append({
            'input': testcase['input'],
            'expected_output': testcase['output'],
            'actual_output': process.stdout.strip(),
            'success': process.stdout.strip() == testcase['output']
        })

    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
