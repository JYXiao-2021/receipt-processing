from flask import Flask, request, jsonify
app = Flask(__name__)

# In-memory storage for receipt data
receipts_data = {}

@app.route('/receipts/process', methods=['POST'])
def process_receipt():
    # Implement the processing logic here
    return jsonify({"id": "example_id"})

@app.route('/receipts/<receipt_id>/points', methods=['GET'])
def get_receipt_points(receipt_id):
    # Implement the retrieval logic here
    return jsonify({"points": 32})

if __name__ == '__main__':
    app.run(debug=True)
