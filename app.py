from flask import Flask, request, jsonify, Response, send_file
from use_model import load_local_model, image_detection, frame_detection, detect_frames, adjust_path_separator
from DataBase.DatabaseManager import DatabaseManager
import csv
import os
from Camera import Camera

app = Flask(__name__)

dir_path = os.path.dirname(os.path.abspath(__file__))
# Initialize Firebase Admin SDK
BUCKET = "database-Token.appspot.com"
CREDENTIAL_PATH = os.path.join(dir_path, os.path.join("DataBase", "database.json"))

manager = DatabaseManager(CREDENTIAL_PATH, BUCKET)


def read_csv_to_dict(filename):
    signs_details = {}
    with open(filename, mode='r', newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            sign = row['Sign']
            description = row['Description']
            image = row['Image']
            signs_details[sign] = {
                'description': description,
                'image': image
            }
    return signs_details


csv_file = os.path.join(dir_path, os.path.join("DataBase", "SignDetails.csv"))
# Create a dictionary to store the data
sign_details = read_csv_to_dict(csv_file)


def model_choose(name):
    path_to_model = None

    if name == 'best_3':
        path_to_model = r'yolov5\runs\train\exp3\weights\best.pt'
    elif name == 'best_11':
        path_to_model = r'yolov5\runs\train\exp11\weights\best.pt'
    elif name == 'best_14':
        path_to_model = r'Models\exp14\weights\best.pt'

    path_to_model = adjust_path_separator(path_to_model)
    abs_path_to_model = os.path.join(dir_path, path_to_model)
    return abs_path_to_model


# Load the YOLOv5 local model
model_choice = "best_14"
model = load_local_model(model_choose(model_choice))
camera = Camera()


@app.route('/detect_image', methods=['POST'])
def detect_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided.'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No image selected for uploading.'}), 400

    try:
        results = image_detection(model, file.stream)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/detect_video')
def detect_video():
    stream = 0
    # Return a multipart response
    return Response(detect_frames(model, stream), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/detect_live', methods=['GET', 'POST'])
def detect_live():
    if request.method == 'POST':
        # Start the webcam and detection process
        stream = request.json.get('stream', 0)  # Defaulting to 0 if not specified
        return jsonify({
            "status": "success",
            "message": "Detection started, retrieve results with a GET request."
        }), 200
    elif request.method == 'GET':
        try:
            camera.initialize_camera()
            frame = camera.capture_frame()
            results = frame_detection(model, frame)
            return jsonify(results), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500


@app.route('/get_image/<image_name>')
def get_image(image_name):
    image_path = os.path.join(os.path.join(dir_path, os.path.join("DataBase", "Meta")), image_name)

    try:
        return send_file(image_path, mimetype='image/png')  # Adjust mimetype according to your image format
    except Exception as e:
        return jsonify({'error': str(e)}), 404


@app.route('/search', methods=['GET'])
def get_sign_details():
    query = request.args.get('query', '').title()  # Normalize input to match keys
    query = query.strip().lower()

    if query in sign_details:
        sign_info = sign_details[query]
        # Generate a URL to access the image
        image_url = request.url_root + 'get_image/' + sign_info['image'].split('/')[
            -1]  # Assuming the image field stores the filename

        response = {  # This will include both the description and the image URL
            "success": True,
            "data": {
                "description": sign_info['description'],
                "image_url": image_url
            }
        }
    else:
        sign = manager.get_sign(query)
        if sign:
            response = {  # This will include both the description and the image URL
                "success": True,
                "data": {
                    "description": sign['description'],
                    "image_url": sign['image_path']
                }
            }
        else:
            response = {
                "success": False,
                "error": "Sign not found"
            }
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
