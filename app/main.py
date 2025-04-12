from flask import Flask, request, jsonify, send_from_directory, render_template
from handlers import generate_presentation_story, create_json_presentation, extract_data_from_files
import os

app = Flask(__name__)


# Serve the index.html for the frontend
@app.route("/", methods=["GET"])
def serve_frontend():
    return render_template("index.html")


# Handle the presentation generation
@app.route("/", methods=["POST"])
async def generate_presentation():
    prompt = request.form["prompt"]
    files = request.files.getlist("files")

    if not files or not prompt:
        return (
            jsonify({"error": "Invalid input. Ensure a valid prompt and files."}),
            400,
        )

    # Save uploaded files
    upload_directory = "uploads"
    if not os.path.exists(upload_directory):
        os.makedirs(upload_directory)

    for file in files:
        file.save(os.path.join(upload_directory, file.filename))

    extracted_data = await extract_data_from_files(upload_directory)
    story = generate_presentation_story(prompt, extracted_data)
    #presentation = create_json_presentation(story)

    # Clean up uploaded files
    for file in files:
        os.remove(os.path.join(upload_directory, file.filename))

    return jsonify({"presentation": story})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
