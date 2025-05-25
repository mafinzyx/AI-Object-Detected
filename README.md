# Image Object Detection Web Application
### 🔗 **Contributors**

[![GitHub - Danylo Zherzdiev](https://img.shields.io/badge/GitHub-Danylo_Zherzdiev-181717?style=for-the-badge&logo=github)](https://github.com/mafinzyx)   [![GitHub - Danylo Lohachov](https://img.shields.io/badge/GitHub-Danylo_Lohachov-181717?style=for-the-badge&logo=github)](https://github.com/eternaki) [![GitHub - Evelina Rylova](https://img.shields.io/badge/GitHub-Evelina_Rylova-181717?style=for-the-badge&logo=github)](https://github.com/peachwat) [![GitHub - Maria Volkova](https://img.shields.io/badge/GitHub-Maria_Volkova-181717?style=for-the-badge&logo=github)](https://github.com/mvollkova)

A web application that uses YOLOv8 for object detection in images. Users can upload images and get real-time object detection results with the ability to highlight specific objects.

## Features

- Upload images for object detection
- Automatic detection of objects in images
- Highlight specific objects in the image
- Modern and responsive UI
- Real-time results

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python run.py
```

4. Open your browser and navigate to `http://localhost:xxxx`

## Usage

1. Click on the upload area to select an image
2. Wait for the object detection to complete
3. Click on any detected object to highlight it in the image
4. Alternatively, type the object name in the search box and press Enter

## Technologies Used

- Flask (Backend)
- YOLOv8 (Object Detection)
- OpenCV (Image Processing)
- Tailwind CSS (Frontend Styling)
- JavaScript (Frontend Logic)

## Project Structure

```
.
├── app/
│   ├── static/
│   │   ├── uploads/      # Uploaded images
│   │   └── results/      # Processed images
│   ├── templates/
│   │   └── index.html    # Main UI
│   ├── models/
│   │   └── image_processor.py  # YOLO integration
│   ├── __init__.py       # Flask app factory
│   └── routes.py         # API endpoints
├── requirements.txt      # Dependencies
└── run.py               # Application entry point
``` 
