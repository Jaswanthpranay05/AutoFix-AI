from flask import Flask, request, jsonify
from flask_cors import CORS
from autocorrector import AdvancedContextAutocorrector

app = Flask(__name__)
CORS(app)

# Initialize autocorrector once
corrector = AdvancedContextAutocorrector()

@app.route("/autocorrect", methods=["POST"])
def autocorrect_api():
    data = request.json
    text = data.get("text", "")
    
    corrected = corrector.autocorrect_sentence(text)
    return jsonify({"corrected": corrected})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
