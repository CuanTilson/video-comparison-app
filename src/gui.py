from tkinter import Tk, Label, filedialog, messagebox
from tkinter import ttk
import cv2
import numpy as np
from video_processor import extract_frames, compare_frames
from utils import generate_report
import webbrowser


class VideoComparisonApp:
    def __init__(self, master):
        self.master = master
        master.title("Video Comparison App")

        self.label = ttk.Label(master, text="Upload Videos for Comparison")
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

        self.view_report_button = ttk.Button(
            master, text="View Report", command=self.view_report, state="disabled"
        )
        self.view_report_button.pack(pady=5)

        self.before_video_path = None
        self.after_video_path = None
        self.report_path = None

    def upload_before_video(self):
        self.before_video_path = filedialog.askopenfilename(
            title="Select Before Video", filetypes=[("Video Files", "*.mp4;*.avi")]
        )
        if self.before_video_path:
            messagebox.showinfo("Video Selected", "Before video uploaded successfully.")

    def upload_after_video(self):
        self.after_video_path = filedialog.askopenfilename(
            title="Select After Video", filetypes=[("Video Files", "*.mp4;*.avi")]
        )
        if self.after_video_path:
            messagebox.showinfo("Video Selected", "After video uploaded successfully.")

    def compare_videos(self):
        if not self.before_video_path or not self.after_video_path:
            messagebox.showerror(
                "Error", "Please upload both videos before comparison."
            )
            return

        frames_before = extract_frames(self.before_video_path)
        frames_after = extract_frames(self.after_video_path)

        differences = compare_frames(frames_before, frames_after)

        if differences:
            self.report_path = generate_report(differences)
            messagebox.showinfo(
                "Comparison Complete",
                f"Differences detected. Report generated at: {self.report_path}",
            )
            self.view_report_button.config(state="normal")
        else:
            messagebox.showinfo(
                "Comparison Complete", "No significant differences detected."
            )

    def view_report(self):
        if self.report_path:
            webbrowser.open(self.report_path)


if __name__ == "__main__":
    root = Tk()
    root.geometry("600x400")  # Set the window size to 600x400
    app = VideoComparisonApp(root)
    root.mainloop()
