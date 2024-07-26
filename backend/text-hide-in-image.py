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

def texthide(imageFile,textMessage,outImage):
    path = get_full_path(imageFile)
    lsb.hide(path,message=textMessage).save(outImage)

app=Flask(__name__)
CORS(app)

@app.route('/run_python', methods=['POST'])
def run_python():
    if not request.is_json:
        return jsonify({'status': 400, 'message': 'Invalid request'}), 400

    data = request.json
    if 'imageName' not in data or 'message' not in data:
        return jsonify({'status': 400, 'message': 'Invalid request'}), 400

    imageFile = data['imageName']
    textMessage = data['message']
    outImage = os.path.join(os.path.dirname(get_full_path(imageFile)), 'output.png')

    try:
        texthide(imageFile, textMessage, outImage)
        return jsonify({'status': 200, 'filename': 'output.png', 'message': 'Success'}), 200
    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({'status': 500, 'message': 'Internal Server Error'}), 500

    
if __name__ == '__main__':
    app.run(debug=True)



