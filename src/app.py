from flask import Flask, request, jsonify
import uuid
from vali import get_total_receipt_points, validate_receipt

app = Flask(__name__)

receipts_data = {}

@app.route("/receipts/process", methods=["POST"])
def process_receipts():
    receipt = request.get_json()
    validation_result = validate_receipt(receipt)
    if not validation_result.is_valid:
        return jsonify(error="The receipt is invalid", message=validation_result.message), 400
    receipt_id = str(uuid.uuid4())
    points = get_total_receipt_points(receipt)
    receipts_data[receipt_id] = points
    return jsonify(id=receipt_id), 201

@app.route("/receipts/<id>/points", methods=["GET"])
def get_points(id):
    points = receipts_data.get(id)
    if points is None:
        return jsonify(error="No receipt found for that id"), 404
    return jsonify(points=points)

if __name__ == "__main__":
    app.run(host='0.0.0.0')



