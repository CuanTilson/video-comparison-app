from tensorflow.keras.models import load_model
import numpy as np


class VideoComparisonModel:
    def __init__(self, model_path):
        self.model = self.load_model(model_path)

    def load_model(self, model_path):
        return load_model(model_path)

    def preprocess_frame(self, frame):
        frame = cv2.resize(frame, (224, 224))  # Resize to match model input
        frame = frame.astype("float32") / 255.0  # Normalize pixel values
        return np.expand_dims(frame, axis=0)  # Add batch dimension

    def predict(self, frame):
        processed_frame = self.preprocess_frame(frame)
        predictions = self.model.predict(processed_frame)
        return predictions

    def compare_frames(self, frame1, frame2):
        prediction1 = self.predict(frame1)
        prediction2 = self.predict(frame2)
        # Implement comparison logic based on predictions
        # This could involve calculating differences or using a threshold
        return prediction1, prediction2
