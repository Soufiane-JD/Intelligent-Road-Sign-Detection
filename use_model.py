import torch
import cv2
import numpy as np
import os
import pathlib
import platform
from PIL import Image

dir_path = os.path.dirname(os.path.abspath(__file__))


# This code is handling cross-platform path compatibility by forcing one type of pathlib path object to behave like
# the other, depending on the operating system
def platform_compatibility():
    plt = platform.system()  # type of operating system on which the Python script is running.
    if plt == 'Windows':
        pathlib.PosixPath = pathlib.WindowsPath  # deploying for Windows
    else:
        pathlib.WindowsPath = pathlib.PosixPath  # deploying for linux


platform_compatibility()


def adjust_path_separator(path):
    plt = platform.system()  # type of operating system on which the Python script is running.
    if plt == 'Windows':
        path = path.replace('/', '\\')
    else:
        path = path.replace('\\', '/')
    return path


def load_local_model(model_path):

    repo_or_dir = os.path.join(dir_path, 'yolov5')  # r'E:\moi\Programming\Python\code\PFE_Final\yolov5'
    try:
        # Check if CUDA (GPU) is available for PyTorch
        torch_available = torch.cuda.is_available()
        print("CUDA available for PyTorch:", torch_available)

        # Check if CUDA (GPU) is available else Set device to CPU
        device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

        # Print the device being used
        print('Using device:', device)

        if os.path.exists(repo_or_dir):
            # Load model
            local_model = torch.hub.load(repo_or_dir, 'custom', path=model_path, source='local', device=device)
        else:
            print("repo or dir YOLO V5 not fond")
            local_model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, device=device)
        return local_model
    except Exception as e:
        print("Error loading model:", e)
        return None


def get_detected_result(model, results):
    result_detection = []
    # Get the detected classes and their confidence scores
    class_indices = results.xyxy[0][:, -1].cpu().numpy().astype(int)
    confidences = results.xyxy[0][:, 4].cpu().numpy()

    # Get the class names if available
    if hasattr(model, 'names'):
        class_names = model.names
    else:
        class_names = None

    # Print the names of detected classes along with bounding boxes
    for idx in class_indices:
        if class_names:
            class_name = class_names[idx]
        else:
            class_name = f"Class {idx}"

    # Print the names and percentages of detected classes along with bounding boxes
    for idx, conf in zip(class_indices, confidences):
        class_name = class_names[idx]
        percentage = f"{conf * 100:.2f}%"
        result_detection.append(f"Detected_class: {class_name}, Confidence: {percentage}")
    return result_detection


def get_The_max_confidence(result_detection):
    # return result_detection
    max_confidence = 50
    max_confidence_class = ''

    for item in result_detection:
        # Extracting confidence value from each item
        confidence = float(item.split(',')[1].split(':')[1].strip().replace('%', ''))

        # Comparing confidence to find the maximum
        if confidence > max_confidence:
            max_confidence = confidence
            max_confidence_class = item.split(',')[0].split(':')[1].strip()
    return {'class': max_confidence_class, 'confidence': str(max_confidence)}


def resize_and_crop(image, target_size):
    if image is None:
        print("Error: Image not found.")
        return None

    # Extract the dimensions of the original image
    height, width = image.shape[:2]
    # print(height, width)
    # If the image is already the target size, return the original image
    if width <= target_size or height <= target_size:
        # print("Image is already at the target size.")
        return image

    # Calculate the scaling factor to scale the image to cover the target size
    scaling_factor = max(target_size / width, target_size / height)
    new_width = int(width * scaling_factor)
    new_height = int(height * scaling_factor)
    # print('new size', new_height, new_width)

    # Resize the image using the scaling factor
    resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LINEAR)

    # Calculate the top-left corner of the crop box
    start_x = (new_width - target_size) // 2
    start_y = (new_height - target_size) // 2

    # Crop the center of the resized image to the target size
    cropped_image = resized_image[start_y:start_y + target_size, start_x:start_x + target_size]

    return cropped_image


def image_detection(model, file_stream):
    result_detection = []
    max_confidence_class = ''
    try:
        # Methode 1
        # Read image from file stream
        file_bytes = np.asarray(bytearray(file_stream.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        # Methode 2
        # image = cv2.imread(file_stream)
        if image is None:  # Check if the image is loaded correctly
            print("Error: Image not loaded")
        else:
            # Convert from BGR to RGB
            frame_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Resize frame to target resolution
            resized_frame = resize_and_crop(frame_rgb, 416)

            # Convert to PIL Image
            # frame = Image.fromarray(resized_frame)
            results = model(frame_rgb)  # model(resized_frame, size=416)

            result_detection = get_detected_result(model, results)
            print("Result: ", result_detection)
            # # Define the window name
            # window_name = 'Image with Detections'
            # # Display Image
            # img_with_detections = np.squeeze(results.render())
            # #img_with_detections = cv2.cvtColor(img_with_detections, cv2.COLOR_RGB2BGR)  # Convert to BGR for OpenCV
            #
            # # Create a named window with specified size
            # cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)  # WINDOW_NORMAL allows resizing
            # cv2.resizeWindow(window_name, 800, 600)
            # cv2.imshow(window_name, img_with_detections)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            max_confidence_class = get_The_max_confidence(result_detection)
    except Exception as e:
        print(f"Error: {e}")
    return max_confidence_class


def detect_frames(model, stream):
    cap = cv2.VideoCapture(stream)  # Start the webcam
    if not cap.isOpened():
        raise RuntimeError("Could not start webcam.")

    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            # Convert from BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Resize frame to target resolution
            # resized_frame = resize_and_crop(frame_rgb, 416)

            # Convert to PIL Image
            frame = Image.fromarray(frame_rgb)

            # Perform detection
            results = model(frame)
            img_with_detections = cv2.cvtColor(np.squeeze(results.render()), cv2.COLOR_RGB2BGR)  # Convert to BGR for OpenCV

            # Convert the image to JPEG format for transmission
            ret, buffer = cv2.imencode('.jpg', img_with_detections)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def real_time_detection(model, stream):
    cap = cv2.VideoCapture(stream)
    if not cap.isOpened():
        raise RuntimeError("Could not start webcam.")

    while True:
        success, frame = cap.read()
        if not success:
            break

        result_detection = []

        if not success:
            break
        else:
            # Convert the colors from BGR to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Resize frame to target resolution
            # resized_frame = resize_and_crop(frame, 416)

            # Perform object detection on the image
            results = model(frame)

            result_detection = get_detected_result(model, results)

            # Define the window name
            window_name = 'Image with Detections'
            # Display Image
            img_with_detections = np.squeeze(results.render())
            img_with_detections = cv2.cvtColor(img_with_detections, cv2.COLOR_RGB2BGR)  # Convert to BGR for OpenCV

            # Create a named window with specified size
            cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)  # WINDOW_NORMAL allows resizing
            cv2.resizeWindow(window_name, 800, 600)
            cv2.imshow(window_name, img_with_detections)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        # Send the detected classes as JSON response
        yield result_detection


def frame_detection(model, frame):
    result_detection = []
    max_confidence_class = ''
    try:
        if frame is None:
            return None
        else:
            # Convert the colors from BGR to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Resize frame to target resolution
            # resized_frame = resize_and_crop(frame, 416)

            # Perform object detection on the image
            results = model(frame)

            result_detection = get_detected_result(model, results)
            print(result_detection)

            # # Define the window name
            # window_name = 'Image with Detections'
            # # Display Image
            # img_with_detections = np.squeeze(results.render())
            # img_with_detections = cv2.cvtColor(img_with_detections, cv2.COLOR_RGB2BGR)  # Convert to BGR for OpenCV
            #
            # # Create a named window with specified size
            # cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)  # WINDOW_NORMAL allows resizing
            # cv2.resizeWindow(window_name, 800, 600)
            # cv2.imshow(window_name, img_with_detections)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            max_confidence_class = get_The_max_confidence(result_detection)
    except Exception as e:
        print(f"Error: {e}")

    # Send the detected classes as JSON response
    return max_confidence_class


def frame_detection_Stream(model, stream):
    result_detection = []
    max_confidence_class = ''
    try:
        cap = cv2.VideoCapture(stream)
        if not cap.isOpened():
            raise RuntimeError("Could not start webcam.")

        success, frame = cap.read()
        cap.release()

        if not success:
            return None
        else:
            # Convert the colors from BGR to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Resize frame to target resolution
            # resized_frame = resize_and_crop(frame, 416)

            # Perform object detection on the image
            results = model(frame)

            result_detection = get_detected_result(model, results)
            print(result_detection)

            # # Define the window name
            # window_name = 'Image with Detections'
            # # Display Image
            # img_with_detections = np.squeeze(results.render())
            # img_with_detections = cv2.cvtColor(img_with_detections, cv2.COLOR_RGB2BGR)  # Convert to BGR for OpenCV
            #
            # # Create a named window with specified size
            # cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)  # WINDOW_NORMAL allows resizing
            # cv2.resizeWindow(window_name, 800, 600)
            # cv2.imshow(window_name, img_with_detections)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            max_confidence_class = get_The_max_confidence(result_detection)
    except Exception as e:
        print(f"Error: {e}")

    # Send the detected classes as JSON response
    return max_confidence_class
