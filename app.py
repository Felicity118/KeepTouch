from flask import Flask, request, jsonify
from friends import execute
app = Flask(__name__)
@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    open=execute()
    return jsonify({"message": f"Message sent successfully: {open}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True,port=5008)