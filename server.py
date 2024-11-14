from flask import Flask, request, jsonify, send_file
from time import  strftime
import os, sys, time, threading
import subprocess
from tts import text_to_speech  # Import from the google_tts file
from flask_cors import CORS
import werkzeug

app = Flask(__name__)

# Dictionary to track the status of video generation by file name
video_status = {}

CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}})

# Define a folder to store uploaded files
UPLOAD_FOLDER = './uploaded_images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
output_video_path=''

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/generate', methods=['POST','OPTIONS' ])
def generate_avatar_video():

    if request.method == 'OPTIONS':
        # This is the preflight request, handle it accordingly
        return _build_cors_preflight_response()

    if request.method == 'POST':
        try:

            # Get the text, gender, and image blob from the JSON request
            text = request.form.get('text')
            gender = request.form.get('voice')
            avatar_image = request.files.get('image')  # This should be the binary blob of the image


            if not text or not gender or not avatar_image:
                return jsonify({"error": "Missing input data"}), 400


            # Save the image file to the server
            image_filename = werkzeug.utils.secure_filename(avatar_image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
            avatar_image.save(image_path)

            # Step 1: Generate Text-to-Speech using Google TTS
            tts_output = text_to_speech(text,gender)

            if not tts_output:
                return jsonify({"error": "Failed to generate speech"}), 500

            # Step 2: Use SadTalker to create the video
            avatar_video_file = generate_sadtalker_video(tts_output, image_path)

            #if not avatar_video:
            #    return jsonify({"error": "Failed to generate avatar video"}), 500
            print(f"Returned to generate_avatar_video")
            print(f"{avatar_video_file}")
            return jsonify({"file_name": avatar_video_file}), 202
            # Step 4: Send the generated video to the user
            #return send_file(avatar_video, mimetype='video/mp4')
            #return jsonify({"Path":avatar_video})

        except Exception as e:
            return jsonify({'error': str(e)}), 500


@app.route('/check-video-status', methods=['GET'])
def check_video_status():
    # Retrieve the file name from the request
    file_name = request.args.get('file_name')

    # Check the status of the requested file
    status = video_status.get(file_name, "not_found")
    
    if video_status[file_name] == "completed":
        # If completed, return the video path or URL
        #video_path = f"/{file_name}"  # Adjust this path as needed
        return jsonify({"status": "completed", "video_path": file_name})
    else:
        # If still in progress, prompt the client to check again later
        return jsonify({"status": "in progress"})

@app.route('/getVideo', methods=['POST'])
def getVideo():
    if request.method == 'OPTIONS':
        # This is the preflight request, handle it accordingly
        return _build_cors_preflight_response()

    if request.method == 'POST':
        try:
            #fileName = request.args.post('fileName')
            # Parse JSON payload
            data = request.get_json()

            # Get the filename from the JSON data
            fileName = data.get('fileName')+".mp4"

            print(f"{fileName}")
            if not fileName:
                print(f"{fileName} not found")
                return jsonify({"error": "Failed to generate avatar video"}), 500
            else:
                # Send the generated video to the user
                print(f"sending {fileName}")
                return send_file(fileName, mimetype='video/mp4')
        except Exception as e:
            print(f"{str(e)}")
            return jsonify({'error': str(e)}), 500

#Function for OPTIONS method
def _build_cors_preflight_response():
    response = jsonify({'message': 'CORS Preflight'})
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    return response

# Function to generate video using SadTalker
def generate_sadtalker_video(mp3_file, avatar_image):
    output_dir = "output_video/"
    os.makedirs(output_dir, exist_ok=True)
    # Run the SadTalker command with conda environment activation
    output_video_path = os.path.join(output_dir,strftime("%Y_%m_%d_%H.%M"))# "avatar_video.mp4")
    thread = threading.Thread(target=run_inference, args=(mp3_file, avatar_image, output_dir,output_video_path))
    thread.start()
    print(f"{output_video_path}")
    print(f"generate_sadtalker_video processing")
    return output_video_path

def run_inference(mp3_file, avatar_image, output_dir, output_video_path):
    try:
        video_status[output_video_path] = "in progress"  # Set initial status as "in progress"
        print(f"Starting video generation")
        command = f"python inference.py --driven_audio {mp3_file} --source_image {avatar_image} --result_dir {output_video_path} --still --preprocess full --enhancer gfpgan"
        subprocess.run(command, shell=True, executable='/bin/bash', check=True)
        video_status[output_video_path] = "completed"  # Mark the status as completed
    except subprocess.CalledProcessError as e:
        print(f"Error running SadTalker: {e}")
        return None


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
