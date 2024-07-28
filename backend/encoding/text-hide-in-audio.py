import wave
import soundfile as sf
from flask import Flask, request,jsonify,send_file
from flask_cors import CORS
import glob
import os

def em_audio(audio, string, output):
  waveaudio = wave.open(audio, mode='rb')
  frame_bytes = bytearray(list(waveaudio.readframes(waveaudio.getnframes())))
  string = string + int((len(frame_bytes)-(len(string)*8*8))/8) *'#'
  bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in string])))
  for i, bit in enumerate(bits):
    frame_bytes[i] = (frame_bytes[i] & 254) | bit
  frame_modified = bytes(frame_bytes)
  with wave.open(output, 'wb') as fd:
    fd.setparams(waveaudio.getparams())
    fd.writeframes(frame_modified)
  waveaudio.close()

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

@app.route('/hide_text', methods=['POST'])
def hide_text():
    try:
        if not request.is_json:
          return jsonify({'status': 400, 'message': 'Invalid request'}), 400

        data = request.json
        if 'audioFile' not in data or 'text' not in data:
            return jsonify({'status': 400, 'message': 'Invalid request'}), 400
        
        filename = data['audioFile']
        message = data['text']
        audio_path = get_full_path(filename)
        if audio_path == "File not found":
            return jsonify({'status': 404, 'message': 'Audio file not found'}), 404
        wav_path = os.path.join(os.path.dirname(audio_path), 'output.wav')
        wavconvert(audio_path)
        em_audio(wav_path, message, 'output_stego.wav')
        return send_file('output_stego.wav', mimetype='audio/wav')
    except Exception as e:
        import traceback
        error_message = traceback.format_exc()
        print(f"Error: {error_message}")
        return jsonify({'status': 500, 'message': 'Internal Server Error'}), 500

if __name__ == '__main__':
   app.run(debug=True)