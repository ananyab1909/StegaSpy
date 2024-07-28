from stegano import lsb
import os
import glob
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

def get_full_path(file_name):
    for root, dirs, files in os.walk(os.getcwd()):
        for file in glob.glob(os.path.join(root, file_name)):
            return os.path.abspath(file)
    return "File not found"

def textreveal(imageFile):
    path = get_full_path(imageFile)
    message= lsb.reveal(imageFile)
    outFile = os.path.join(os.path.dirname(path), 'decode.txt')
    with open(outFile, 'w') as f:
        f.write(message)

app=Flask(__name__)
CORS(app)

@app.route('/decode_image', methods=['POST'])
def decode_image():
    if not request.is_json:
        return jsonify({'status': 400, 'message': 'Invalid request'}), 400

    data = request.json
    if 'imageName' not in data:
        return jsonify({'status': 400, 'message': 'Invalid request'}), 400

    imageFile = data['imageName']

    try:
        textreveal(imageFile)
        return jsonify({'status': 200, 'filename': 'decode.txt', 'message': 'Success'}), 200
    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({'status': 500, 'message': 'Internal Server Error'}), 500

    
if __name__ == '__main__':
    app.run(debug=True)



