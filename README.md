# Intelligent Road Sign Detection

This project focuses on real-time detection and recognition of road signs using deep learning. The system is deployed on a Raspberry Pi, with optional Firebase integration for data management, and includes an admin app for monitoring. A user-friendly interface is built with Flutter. The application detects road signs from an image or video stream and also allows users to search for and understand road signs.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

- Real-time road sign detection using deep learning.
- Deployed on Raspberry Pi for edge computing.
- Optional Firebase integration for managing data.
- Admin app for monitoring and control.
- User-friendly interface developed with Flutter.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Soufiane-JD/Intelligent-Road-Sign-Detection.git
   ```
2. **Navigate to the project directory:**
   ```bash
   cd Intelligent-Road-Sign-Detection
   ```
3. **Set up the virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
4. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the detection model:**
   ```bash
   python app.py
   ```
2. **Use the mobile app for detections:**
   - Install the app.
   - Go to settings and change the server URL to the Flask application URL.

3. **Detection of Road Signs from an Image:**
   - **Camera Button:** Activates the device's camera, allowing users to take a new photo.
   - **Gallery Button:** Provides access to the device's gallery, enabling users to select an existing image.
   - **Voice Activation:** A checkbox that activates the application's text-to-speech functionality, announcing the names of detected road signs aloud.
   - **Detection Results:** Displays the detection results obtained from the camera or an image from the gallery, including the type of sign and its accuracy.
      <img src="https://github.com/user-attachments/assets/c34ac24e-bc75-48e0-b0d8-030ffdc08b76" alt="Detection from an Image" width="200">

5. **Start Real-Time Road Sign Detection:**
   **Buttons:**
   
   - **Direct Activation Button:** Activates the camera in video mode for real-time detection of road signs.
   - **Direct Deactivation Button:** Stops the real-time detection of road signs.
   
   **Voice Activation:** A checkbox that enables the text-to-speech functionality.
   
   **Real-Time Detection Results:** Displays the real-time results, showing detected road signs on the screen with their class and accuracy.
      <img src="https://github.com/user-attachments/assets/ee26e0fc-e1a0-4fef-a14d-82b1cd257327" alt="Real-Time Detection" width="200">

## Project Structure

```
├── models/             # Trained models
├── DataBase/           # Classes for interacting with the database
│   └── DataBaseAdminApp.py        # Admin app code
├── camera.py           # Class for using the camera
├── use_model.py        # Detection logic
├── meta/               # Metadata for road signs
├── README.md           # This README file
└── requirements.txt    # Python dependencies
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a Pull Request.
 
