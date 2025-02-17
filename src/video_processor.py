import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
from tensorflow.keras.applications import MobileNet
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.models import load_model


class VideoProcessor:
    def __init__(self, model_path=None):
        if model_path:
            self.model = load_model(model_path)
        else:
            self.model = MobileNet(weights="imagenet", include_top=False)

    def extract_frames(self, video_path, frame_rate=1):
        video_capture = cv2.VideoCapture(video_path)
        frames = []
        fps = video_capture.get(cv2.CAP_PROP_FPS)
        frame_interval = int(fps / frame_rate)

        while True:
            ret, frame = video_capture.read()
            if not ret:
                break
            if int(video_capture.get(cv2.CAP_PROP_POS_FRAMES)) % frame_interval == 0:
                frames.append(frame)

        video_capture.release()
        return frames

    def compare_frames_ssim(self, frame1, frame2):
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        score, diff = ssim(gray1, gray2, full=True)
        return score, diff

    def compare_frames_deep_learning(self, frame1, frame2):
        frame1_resized = cv2.resize(frame1, (224, 224))
        frame2_resized = cv2.resize(frame2, (224, 224))
        frame1_normalized = preprocess_input(frame1_resized)
        frame2_normalized = preprocess_input(frame2_resized)

        prediction1 = self.model.predict(np.expand_dims(frame1_normalized, axis=0))
        prediction2 = self.model.predict(np.expand_dims(frame2_normalized, axis=0))

        return prediction1, prediction2

    def highlight_differences(self, frame1, frame2, diff_threshold=0.98):
        score, diff = self.compare_frames_ssim(frame1, frame2)
        print(f"SSIM score: {score}")  # Debug statement
        if score < diff_threshold:
            frame1_highlighted, frame2_highlighted = self._highlight_differences(
                frame1, frame2, diff
            )
            return frame1_highlighted, frame2_highlighted, diff
        return frame1, frame2, None

    def _highlight_differences(self, frame1, frame2, diff):
        diff = (diff * 255).astype(np.uint8)
        gray = cv2.cvtColor(diff, cv2.COLOR_GRAY2BGR)  # Ensure single-channel image
        gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)  # Convert to single-channel image
        _, thresh = cv2.threshold(
            gray, 30, 255, cv2.THRESH_BINARY_INV
        )  # Inverted threshold value
        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        bounding_boxes = []
        for contour in contours:
            if cv2.contourArea(contour) > 100:  # Lowered minimum area to consider
                x, y, w, h = cv2.boundingRect(contour)
                bounding_boxes.append([x, y, x + w, y + h])

        # Merge overlapping bounding boxes using Non-Maximum Suppression (NMS)
        merged_boxes = self.non_max_suppression(bounding_boxes, overlap_threshold=0.5)

        for x_min, y_min, x_max, y_max in merged_boxes:
            cv2.rectangle(frame1, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
            cv2.rectangle(frame2, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

        return frame1, frame2

    def non_max_suppression(self, boxes, overlap_threshold=0.5):
        if len(boxes) == 0:
            return []

        boxes = np.array(boxes)
        x1 = boxes[:, 0]
        y1 = boxes[:, 1]
        x2 = boxes[:, 2]
        y2 = boxes[:, 3]

        areas = (x2 - x1 + 1) * (y2 - y1 + 1)
        order = areas.argsort()[::-1]

        keep = []
        while order.size > 0:
            i = order[0]
            keep.append(i)
            xx1 = np.maximum(x1[i], x1[order[1:]])
            yy1 = np.maximum(y1[i], y1[order[1:]])
            xx2 = np.minimum(x2[i], x2[order[1:]])
            yy2 = np.minimum(y2[i], y2[order[1:]])

            w = np.maximum(0, xx2 - xx1 + 1)
            h = np.maximum(0, yy2 - yy1 + 1)
            overlap = (w * h) / areas[order[1:]]

            order = order[np.where(overlap <= overlap_threshold)[0] + 1]

        return boxes[keep].tolist()

    def process_videos(self, video1_path, video2_path):
        frames1 = self.extract_frames(video1_path)
        frames2 = self.extract_frames(video2_path)
        results = []

        for frame1, frame2 in zip(frames1, frames2):
            original_frame1, original_frame2, highlighted_frame = (
                self.highlight_differences(frame1, frame2)
            )
            results.append((original_frame1, original_frame2, highlighted_frame))

        return results
