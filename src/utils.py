def extract_frames(video_path, timestamps):
    import cv2

    frames = []
    cap = cv2.VideoCapture(video_path)

    for timestamp in timestamps:
        cap.set(cv2.CAP_PROP_POS_MSEC, timestamp * 1000)  # Convert to milliseconds
        ret, frame = cap.read()
        if ret:
            frames.append(frame)

    cap.release()
    return frames


def generate_report(differences, output_path):
    from fpdf import FPDF
    import cv2
    import os

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Video Comparison Report", ln=True, align="C")
    pdf.cell(200, 10, txt="", ln=True)  # Empty line

    for i, (frame1, frame2, diff) in enumerate(differences):
        pdf.cell(200, 10, txt=f"Difference detected in frame {i+1}", ln=True)

        # Save the original frames and the difference image to temporary files
        frame1_path = f"frame1_{i+1}.png"
        frame2_path = f"frame2_{i+1}.png"
        diff_image_path = f"diff_{i+1}.png"

        cv2.imwrite(frame1_path, frame1)
        cv2.imwrite(frame2_path, frame2)
        if diff is not None:
            cv2.imwrite(diff_image_path, diff)

        # Add the images to the PDF
        pdf.image(frame1_path, x=10, y=None, w=60)
        pdf.image(frame2_path, x=80, y=None, w=60)
        if diff is not None:
            pdf.image(diff_image_path, x=150, y=None, w=60)

        # Remove the temporary files
        os.remove(frame1_path)
        os.remove(frame2_path)
        if diff is not None:
            os.remove(diff_image_path)

    pdf.output(output_path)


def save_image(image, path):
    import cv2

    cv2.imwrite(path, image)


def load_model(model_path):
    from tensorflow.keras.models import load_model

    return load_model(model_path)


def preprocess_image(image):
    import cv2
    import numpy as np

    image = cv2.resize(image, (224, 224))  # Resize for model input
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    return image / 255.0  # Normalize pixel values


def highlight_differences(original, modified, threshold=30):
    import cv2
    import numpy as np

    diff = cv2.absdiff(original, modified)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) > 500:  # Minimum area to consider
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(original, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.rectangle(modified, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return original, modified
