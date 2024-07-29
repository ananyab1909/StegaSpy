from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import docx
import glob
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['Steganography']
collection = db['text-decode']

def get_full_path(file_name):
    for root, dirs, files in os.walk(os.getcwd()):
        for file in glob.glob(os.path.join(root, file_name)):
            return os.path.abspath(file)
    return "File not found"

def extract_secret_message(file_path):
    path = get_full_path(file_path)
    doc = docx.Document(path)

    secret_message = ''

    for para in doc.paragraphs:
        for run in para.runs:
            if run.font.size == docx.shared.Pt(10):
                secret_message += run.text
    
    outFile = os.path.join(os.path.dirname(path), 'secret-message.txt')
    with open(outFile, 'w') as f:
        f.write(secret_message)

app=Flask(__name__)
CORS(app)

@app.route('/decoded_from_text', methods=['POST'])
def decoded_from_text() :
    try:
        if not request.is_json:
          return jsonify({'status': 400, 'message': 'Invalid request'}), 400
        
        data = request.json
        if 'textFile' not in data:
            return jsonify({'status': 400, 'message': 'Invalid request'}), 400
        
        docFile = data['textFile']
        docPath = get_full_path(docFile)
        
        if docPath == "File not found":
            return jsonify({'status': 404, 'essage': 'Text file not found'}), 404

        try:
            extract_secret_message(docPath)

            mongoTextDecode = {
                "textFile" : docFile,
                "outputFile" : "secret-message.txt",
            }

            result = collection.insert_one(mongoTextDecode)
            collection.update_one({"_id": result.inserted_id}, {"$set": {"created_at": {"$currentDate": {"type": "date"}}}})

            return jsonify({'status': 200, 'filename': 'secret-message.txt', 'essage': 'Success'}), 200
        
        except Exception as e:
            print(f"Error processing request: {e}")
            return jsonify({'status': 500, 'message': 'Internal Server Error'}), 500

        
    except Exception as e:
        import traceback
        error_message = traceback.format_exc()
        print(f"Error: {error_message}")
        return jsonify({'status': 500, 'message': 'Internal Server Error'}), 500
    
if __name__ == '__main__':
    app.run(debug=True)
