from flask import Flask, jsonify
from flask_cors import CORS
import subprocess

app = Flask(__name__)

# Allow all origins (your webapp runs on a different port → required)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/shutdown", methods=["POST"])
def shutdown():
    try:
        # Run shutdown command without password (sudoers rule required)
        subprocess.Popen(["sudo", "shutdown", "-h", "now"])
        return jsonify({"status": "ok", "message": "Shutting down"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    # Runs on port 8080 (systemd handles this normally)
    app.run(host="0.0.0.0", port=8080)