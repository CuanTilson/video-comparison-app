# Video Comparison Application

<!-- This project is a video comparison application designed to help landlords and tenants detect differences between two videos of a rental accommodation. The application allows users to upload a "before" and "after" video, extracts frames at the same timestamps, and compares them using advanced image processing techniques. -->

## Features

- Upload two video files: one before and one after the rental period.
- Extract frames from both videos at the same timestamps.
- Compare frames using:
  - Structural Similarity Index (SSIM)
  - Deep learning models (e.g., pre-trained ResNet or MobileNet)
- Highlight detected differences such as:
  - Furniture movement
  - New damages (cracks, stains, etc.)
- Interactive GUI or web app for user interaction.
- Export a report summarizing the detected changes, including marked images or a PDF.

## Requirements

To run this application, you need to install the following dependencies:

- OpenCV
- TensorFlow
- Flask
- Tkinter or PyQt (for GUI)
- Other necessary libraries

You can install the required packages using the following command:

```
pip install -r requirements.txt
```

## Usage

1. Clone the repository:

   ```
   git clone <repository-url>
   cd video-comparison-app
   ```

2. Install the required dependencies.

3. Run the application:

   ```
   python src/main.py
   ```

4. Upload the two video files when prompted.

5. View the detected changes in the application interface.

6. Export the report summarizing the changes.

## Project Structure

```
video-comparison-app
├── src
│   ├── main.py          # Entry point of the application
│   ├── video_processor.py # Functions for video frame extraction and comparison
│   ├── model.py         # Deep learning model architecture and prediction functions
│   ├── gui.py           # Graphical user interface implementation
│   ├── utils.py         # Utility functions for common tasks
│   └── static
│       ├── css
│       │   └── styles.css # CSS styles for the web app
│       └── js
│           └── scripts.js  # JavaScript for frontend interactions
├── models
│   └── pretrained_model.h5 # Pre-trained deep learning model
├── templates
│   └── index.html         # HTML template for the web app
├── requirements.txt        # List of dependencies
├── README.md               # Project documentation
└── report
    └── sample_report.pdf   # Sample report of detected changes
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.
