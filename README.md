
# Intelligent Road Sign Detection

This project is focused on real-time detection and recognition of road signs using deep learning. The system is deployed on a Raspberry Pi, with Firebase integration for data management(is not necessary for son fonctionnement), and includes an admin app for monitoring. A user-friendly interface is built with Flutter. The application will detect road signs from an image or video stream and also allows users to search for and understand road signs.

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
- Firebase integration for managing data.
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
2. **Use mobile app for make detections:**
   - Instale app
   - go to settings and change server url to url for flask appliction 

3. **Start detection of Road Signs from an Image:**
      <img src="[https://example.com/image.png](https://github.com/user-attachments/assets/c34ac24e-bc75-48e0-b0d8-030ffdc08b76)" alt="Example Image" width="300">
      
   - 
3. **Start Real-Time Road Sign Detection:**
   <img src="[https://example.com/image.png](https://github.com/user-attachments/assets/ee26e0fc-e1a0-4fef-a14d-82b1cd257327)" alt="Example Image" width="300">

   - 

## Project Structure

```
├── models/             # Trained models
├── DataBase/           # Classes pour interaction with dataBase
      └── DataBaseAdminApp.py        # Admin app code
├── camera.py           # Class for using the camera
├── use_model.py        # Detection logic
├── meta/                   # Metadata for road signs
├── README.md               # This README file
└── requirements.txt        # Python dependencies
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a Pull Request.
