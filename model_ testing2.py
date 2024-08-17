import time

import torch
import numpy as np
import cv2
from matplotlib import pyplot as plt
from use_model import load_local_model, resize_and_crop
import csv
import os

# Path to the CSV file
csv_file = r"/DataBase/signnames.csv"


def get_name_of_class(csv_path):
    data_dict = {}
    # Open the CSV file and read its contents
    with open(csv_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            class_id = row['ClassId']
            sign_name = row['SignName']
            data_dict[class_id] = sign_name
    return data_dict


# Create a dictionary to store the data
data_dict = get_name_of_class(csv_file)


def parse_detection(detection):
    # Extract the parts of the string
    class_part, conf_part = detection.split(", ")
    detected_class = class_part.split(": ")[1]
    confidence = float(conf_part.split(": ")[1].replace('%', ''))
    return detected_class, confidence\


def get_max_detection(detections):
    if not detections:
        return None
    # Convert all detections to (class, confidence) tuples
    parsed_detections = [parse_detection(detection) for detection in detections]

    # Find the detection with the maximum confidence
    max_detection = max(parsed_detections, key=lambda x: x[1])
    if max_detection[1] > 50:
        # Format the output
        return f'Detected_class: {max_detection[0]}, Confidence: {max_detection[1]:.2f}%'
    else:
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
        class_index = class_names[idx]
        percentage = f"{conf * 100:.2f}%"
        #class_name = data_dict[class_index]
        class_name = class_index
        result_detection.append(f"Detected_class: {class_name}, Confidence: {percentage}")
    return result_detection

def live_detection(model, model2, model3):
    # Start capturing video from the webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open video device.")
        return

    # Set properties. Each setting is a 'property_id' and a value
    #cap.set(3, 416)  # Set the width of the capture to 416 pixels
    #cap.set(4, 416)  # Set the height of the capture to 416 pixels

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Can't receive frame (stream end?). Exiting ...")
            break

        # Convert frame to RGB (from BGR)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Resize frame to target resolution
        resized_frame = resize_and_crop(frame_rgb, 416)

        # time.sleep(2)
        # Perform detection
        results = model(frame_rgb, size=416)
        results2 = model2(frame_rgb, size=416)
        results3 = model3(frame_rgb, size=416)
        results4 = model3(frame_rgb)

        result_detection = get_detected_result(model, results)
        result_detection2 = get_detected_result(model2, results2)
        result_detection3 = get_detected_result(model3, results3)
        result_detection4 = get_detected_result(model3, results4)

        results_max = get_max_detection(result_detection)
        results_max2 = get_max_detection(result_detection2)
        results_max3 = get_max_detection(result_detection3)
        results_max4 = get_max_detection(result_detection4)
        if results_max or results_max2 or results_max3 or results_max4:
            print("========================================================")
            print("model exp3: ", results_max)
            print("model exp11: ", results_max2)
            print("model exp14: ", results_max3)
            print("model exp14(Resize): ", results_max4)

        # Render results back onto the frame
        frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)  # Convert RGB back to BGR for OpenCV

        # Define the window name
        window_name = 'Image with Detections'
        # Display Image
        img_with_detections = np.squeeze(results3.render())
        img_with_detections = cv2.cvtColor(img_with_detections, cv2.COLOR_RGB2BGR)  # Convert to BGR for OpenCV

        # Create a named window with specified size
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)  # WINDOW_NORMAL allows resizing
        cv2.resizeWindow(window_name, 800, 600)
        cv2.imshow(window_name, img_with_detections)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


def from_img(model, model2, model3, image_path):
    # Load the image
    with open(image_path, 'rb') as f:
        image_data = f.read()

    image_array = np.frombuffer(image_data, np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    if image is None:  # Check if the image is loaded correctly
        print("Error: Image not loaded")
        return

    # Set properties. Each setting is a 'property_id' and a value
    #cap.set(3, 416)  # Set the width of the capture to 416 pixels
    #cap.set(4, 416)  # Set the height of the capture to 416 pixels

    # Convert frame to RGB (from BGR)
    frame_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Resize frame to target resolution
    resized_frame = resize_and_crop(frame_rgb, 416)

    # Perform detection
    results = model(image, size=416)
    results2 = model3(frame_rgb, size=416)
    results3 = model3(resized_frame, size=416)

    result_detection = get_detected_result(model, results)
    result_detection2 = get_detected_result(model3, results2)
    result_detection3 = get_detected_result(model3, results3)

    results_max = get_max_detection(result_detection)
    results_max2 = get_max_detection(result_detection2)
    results_max3 = get_max_detection(result_detection3)
    if results_max or results_max2 or results_max3:
        print("========================================================")
        print("model exp3: ", results_max)
        print("model exp11: ", results_max2)
        print("model exp14: ", results_max3)


    # Render results back onto the frame
    frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)  # Convert RGB back to BGR for OpenCV

    # Define the window name
    window_name = 'Image with Detections'
    # Display Image
    #img_with_detections = np.squeeze(results.render())
    img_with_detections = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # Convert to BGR for OpenCV

    # Create a named window with specified size
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)  # WINDOW_NORMAL allows resizing
    cv2.resizeWindow(window_name, 800, 600)
    cv2.imshow(window_name, image)
    cv2.waitKey(0)  # Wait for a key press to go to the next image



# Example usage
model_path = r'E:\moi\Programming\Python\code\PFE_Final\yolov5\runs\train\exp3\weights\best.pt'  # Update this path
model = load_local_model(model_path)
model_path2 = r'E:\moi\Programming\Python\code\PFE_Final\yolov5\runs\train\exp11\weights\best.pt'  # Update this path
model2 = load_local_model(model_path2)
model_path3 = r'E:\moi\Programming\Python\code\PFE_Final\yolov5\runs\train\exp14\weights\best.pt'  # Update this path
model3 = load_local_model(model_path3)
#live_detection(model, model2)

def from_folder(folder_path):
    for filename in os.listdir(folder_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):  # Check for image files
                image_path = os.path.join(folder_path, filename)
                from_img(model, model2, model3, image_path)
folder_path = r'E:\moi\9raya\Karima\Détection_et_Reconnaissnace_des_panneaux_de_signalisation\DataSet\test_images'
# from_folder(folder_path)

live_detection(model, model2, model3)
