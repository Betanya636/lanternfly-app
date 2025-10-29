from flask import Flask, request, jsonify, render_template
import os
from azure.storage.blob import BlobServiceClient
from datetime import datetime
from dotenv import load_dotenv

# -----------------------------
# Load .env explicitly
# -----------------------------
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if not load_dotenv(dotenv_path):
    raise FileNotFoundError(f".env file not found at {dotenv_path}")

AZURE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
if AZURE_CONNECTION_STRING is None:
    raise ValueError("AZURE_STORAGE_CONNECTION_STRING not found in .env")

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
    # code to save file to Azure
    return jsonify(ok=True, url="...")

        blob_name = f"{datetime.utcnow().strftime('%Y%m%dT%H%M%S')}-{file.filename}"
        blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=blob_name)
        blob_client.upload_blob(file, overwrite=True)

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
