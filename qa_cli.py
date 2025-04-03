from flask import Flask, request, jsonify
from qa_model import QA_MODEL

app = Flask(__name__)
model = QA_MODEL()

@app.route("/qa", methods=["POST"])
def parse_string():
    data = request.get_json()

    if "text" not in data:
        return jsonify({"error": "No text provided"}), 400

    input = data["text"]

    doc = model.query_doc(input)
    response = {
        "received_string": input,
        "doc": doc[0].split('&&&')[1],
    }

    return jsonify(response), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
