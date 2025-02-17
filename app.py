from flask import Flask, render_template, request, jsonify, send_file
import os
from werkzeug.utils import secure_filename
from src.video_processor import VideoProcessor
from src.utils import generate_report

app = Flask(__name__, static_folder="src/static", static_url_path="/static")
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["ALLOWED_EXTENSIONS"] = {"mp4", "avi"}

video_processor = VideoProcessor(model_path=None)


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
    )


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_videos():
    if "video_before" not in request.files or "video_after" not in request.files:
        return jsonify({"error": "No video files provided"}), 400

    video_before = request.files["video_before"]
    video_after = request.files["video_after"]

    if (
        video_before
        and allowed_file(video_before.filename)
        and video_after
        and allowed_file(video_after.filename)
    ):
        filename_before = secure_filename(video_before.filename)
        filename_after = secure_filename(video_after.filename)
        path_before = os.path.join(app.config["UPLOAD_FOLDER"], filename_before)
        path_after = os.path.join(app.config["UPLOAD_FOLDER"], filename_after)
        video_before.save(path_before)
        video_after.save(path_after)

        differences = video_processor.process_videos(path_before, path_after)
        report_path = os.path.join(app.config["UPLOAD_FOLDER"], "report.pdf")
        generate_report(differences, report_path)

        # Debugging statement
        print("Report generated at:", report_path)

        return jsonify(
            {
                "report_url": f"/download/{os.path.basename(report_path)}",
            }
        )

    return jsonify({"error": "Invalid file format"}), 400


@app.route("/download/<filename>")
def download_report(filename):
    return send_file(
        os.path.join(app.config["UPLOAD_FOLDER"], filename), as_attachment=True
    )


if __name__ == "__main__":
    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        os.makedirs(app.config["UPLOAD_FOLDER"])
    app.run(debug=True)
