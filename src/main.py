import cv2
import numpy as np
from tkinter import Tk, Label, filedialog
from tkinter import ttk
from video_processor import VideoProcessor
from utils import generate_report
import webbrowser


class VideoComparisonApp:
    def __init__(self, master):
        self.master = master
        master.title("Video Comparison App")

        self.label = ttk.Label(master, text="Upload two videos to compare:")
        self.label.pack(pady=10)

        self.upload_before_button = ttk.Button(
            master, text="Upload Before Video", command=self.upload_before_video
        )
        self.upload_before_button.pack(pady=5)

        self.upload_after_button = ttk.Button(
            master, text="Upload After Video", command=self.upload_after_video
        )
        self.upload_after_button.pack(pady=5)

        self.compare_button = ttk.Button(
            master, text="Compare Videos", command=self.compare_videos
        )
        self.compare_button.pack(pady=5)

        self.report_button = ttk.Button(
            master, text="Generate Report", command=self.generate_report
        )
        self.report_button.pack(pady=5)

        self.view_report_button = ttk.Button(
            master, text="View Report", command=self.view_report, state="disabled"
        )
        self.view_report_button.pack(pady=5)

        self.before_video_path = None
        self.after_video_path = None
        self.report_path = None
        self.video_processor = VideoProcessor(
            model_path=None  # Set to None to use the default MobileNet model
        )

    def upload_before_video(self):
        self.before_video_path = filedialog.askopenfilename(
            title="Select Before Video", filetypes=[("Video Files", "*.mp4;*.avi")]
        )
        print(f"Before video uploaded: {self.before_video_path}")

    def upload_after_video(self):
        self.after_video_path = filedialog.askopenfilename(
            title="Select After Video", filetypes=[("Video Files", "*.mp4;*.avi")]
        )
        print(f"After video uploaded: {self.after_video_path}")

    def compare_videos(self):
        if self.before_video_path and self.after_video_path:
            differences = self.video_processor.process_videos(
                self.before_video_path, self.after_video_path
            )
            print("Comparison complete. Differences detected:", differences)
        else:
            print("Please upload both videos before comparing.")

    def generate_report(self):
        if self.before_video_path and self.after_video_path:
            differences = self.video_processor.process_videos(
                self.before_video_path, self.after_video_path
            )
            self.report_path = "report.pdf"  # Specify the output path for the report
            generate_report(differences, self.report_path)
            print(f"Report generated: {self.report_path}")
            self.view_report_button.config(state="normal")
        else:
            print("Please upload both videos before generating a report.")

    def view_report(self):
        if self.report_path:
            webbrowser.open(self.report_path)


if __name__ == "__main__":
    root = Tk()
    root.geometry("600x400")  # Set the window size to 600x400
    app = VideoComparisonApp(root)
    root.mainloop()
