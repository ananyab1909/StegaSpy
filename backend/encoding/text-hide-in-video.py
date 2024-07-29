from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import glob
import os
from moviepy.editor import VideoFileClip, ImageClip, ImageSequenceClip
import numpy as np
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['Steganography']
collection = db['video-encode']

def video_hide(inputVideo,text,outputVideo) :
    video = VideoFileClip(inputVideo)
    binary_text = ''.join(format(ord(i), '08b') for i in text)
    frames = []
    for frame in video.iter_frames():
        frame_array = np.array(frame)
        for i in range(len(binary_text)):
            x, y = i // 8, i % 8
            pixel = frame_array[x, y, 0]  
            if binary_text[i] == '1':
                pixel = pixel | 1 
            else:
                pixel = pixel & 0xFE  
            frame_array[x, y, 0] = pixel
        frame = ImageClip(frame_array)
        frames.append(frame_array)

    final_video = ImageSequenceClip(frames, fps=video.fps)
    final_video.write_videofile(outputVideo)  

def get_full_path(file_name):
    for root, dirs, files in os.walk(os.getcwd()):
        for file in glob.glob(os.path.join(root, file_name)):
            return os.path.abspath(file)
    return "File not found"

app=Flask(__name__)
CORS(app)

@app.route('/encode_video', methods=['POST']) 
def encode_video() :
    try:
        if not request.is_json:
          return jsonify({'status': 400, 'message': 'Invalid request'}), 400
        
        data = request.json
        if 'videoFile' not in data or 'secretMessage' not in data:
            return jsonify({'status': 400, 'message': 'Invalid request'}), 400
        
        filename = data['videoFile']
        message = data['secretMessage']

        video_path = get_full_path(filename)

        if video_path == "File not found":
            return jsonify({'status': 404, 'message': 'Video file not found'}), 404
        
        inputPath = video_path
        output_path = os.path.join(os.path.dirname(video_path), 'output_stego.mp4')
        video_hide(inputPath, message, output_path)

        mongoVideoDecode = {
            "videoFile" : filename,
            "secretMessage" : message,
            "outputFile" : "output_stego.mp4",
        }

        result = collection.insert_one(mongoVideoDecode)
        collection.update_one({"_id": result.inserted_id}, {"$set": {"created_at": {"$currentDate": {"type": "date"}}}})

        return send_file(output_path, mimetype='video/mp4')

    except Exception as e:
        import traceback
        error_message = traceback.format_exc()
        print(f"Error: {error_message}")
        return jsonify({'status': 500, 'message': 'Internal Server Error'}), 500
    
if __name__ == '__main__':
    app.run(debug=True)