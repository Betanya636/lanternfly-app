from flask import Flask, request, jsonify, render_template
import os
from azure.storage.blob import BlobServiceClient
from datetime import datetime
from dotenv import load_dotenv

# Try loading from .env (for local use), but don’t crash if it’s missing
load_dotenv()

AZURE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

if not AZURE_CONNECTION_STRING:
    raise ValueError("Missing Azure connection string. Set AZURE_STORAGE_CONNECTION_STRING in Azure App Settings.")

# -----------------------------
# Flask & Azure setup
# -----------------------------
app = Flask(__name__)

CONTAINER_NAME = "lanternfly-images-306ygb5c"
blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)

# -----------------------------
# Routes
# -----------------------------
@app.get("/")
def index():
    return render_template("index.html")

@app.post("/api/v1/upload")
def upload():
    f = request.files.get("file")
    if not f:
        return jsonify({"ok": False, "error": "No file uploaded"}), 400

    try:
        # Proper indentation inside try block
        blob_name = f"{datetime.utcnow().strftime('%Y%m%dT%H%M%S')}-{f.filename}"
        blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=blob_name)
        blob_client.upload_blob(f, overwrite=True)

        return jsonify({"ok": True, "url": blob_client.url})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})

@app.get("/api/v1/gallery")
def gallery():
    # code to list images in Azure Blob
    return jsonify(ok=True, gallery=[...])

# -----------------------------
# Run Flask
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
