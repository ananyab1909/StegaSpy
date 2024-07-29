import wave
import soundfile as sf
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import glob
import os
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['Steganography']
collection = db['audio-decode']

def ex_msg(audio):
    path = os.path.abspath(audio)
    waveaudio = wave.open(audio, mode='rb')
    frame_bytes = bytearray(list(waveaudio.readframes(waveaudio.getnframes())))
    extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
    string = "".join(chr(int("".join(map(str,extracted[i:i+8])),2)) for i in range(0,len(extracted),8))
    message = string.split("###")[0]
    outFile = os.path.join(os.path.dirname(path), 'audio-decoded.txt')
    with open(outFile, 'w') as f:
        f.write(message)
    waveaudio.close()

def find_file(file_name):
    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            if file == file_name:
                return os.path.abspath(os.path.join(root, file))
    return "File not found"

def is_wav_file(file_path):
    return file_path.endswith('.wav')

def wavconvert(file):
  with sf.SoundFile(file, 'r') as f:
    data = f.read()

  with sf.SoundFile('output.wav', 'w', samplerate=f.samplerate, channels=f.channels, subtype='PCM_16') as f:
      f.write(data)

def get_full_path(file_name):
    for root, dirs, files in os.walk(os.getcwd()):
        for file in glob.glob(os.path.join(root, file_name)):
            return os.path.abspath(file)
    return "File not found"


app=Flask(__name__)
CORS(app)

@app.route('/decode_audio', methods=['POST']) 
def decode_audio() :
    try:
        if not request.is_json:
          return jsonify({'status': 400, 'essage': 'Invalid request'}), 400

        data = request.json
        if 'audioFile' not in data:
            return jsonify({'status': 400, 'essage': 'Invalid request'}), 400
        
        filename = data['audioFile']
        audio_path = find_file(filename)

        if audio_path == "File not found":
            return jsonify({'status': 404, 'essage': 'Audio file not found'}), 404
        
        if is_wav_file(audio_path):
            ex_msg(audio_path)

            mongoAudioDecode = {
                "audioFile" : filename,
                "outputFile" : "audio-decoded.txt",
            }

            result = collection.insert_one(mongoAudioDecode)
            collection.update_one({"_id": result.inserted_id}, {"$set": {"created_at": {"$currentDate": {"type": "date"}}}})

            return jsonify({'status': 200, 'filename': 'audio-decoded.txt', 'essage': 'Success'}), 200
        elif audio_path.endswith('.mp3'):
            wavconvert(audio_path)
            ex_msg('output.wav')

            mongoAudioDecode = {
                "audioFile" : filename,
                "outputFile" : "audio-decoded.txt",
            }

            result = collection.insert_one(mongoAudioDecode)
            collection.update_one({"_id": result.inserted_id}, {"$set": {"created_at": {"$currentDate": {"type": "date"}}}})

            return jsonify({'status': 200, 'filename': 'audio-decoded.txt', 'essage': 'Success'}), 200

        else:
            return jsonify({'status': 400, 'essage': 'Only WAV and MP3 files are supported'}), 400
        
        

    except Exception as e:
        import traceback
        error_message = traceback.format_exc()
        print(f"Error: {error_message}")
        return jsonify({'status': 500, 'essage': 'Internal Server Error'}), 500
    
if __name__ == '__main__':
    app.run(debug=True)