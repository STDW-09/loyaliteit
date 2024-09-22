from flask import Flask, request, jsonify

app = Flask(__name__)

customers = {}

class Customer:
    def __init__(self, name):
        self.name = name
        self.points = 0
        self.purchases = []

    def make_purchase(self, amount):
        self.purchases.append(amount)
        earned_points = self.calculate_points(amount)
        self.points += earned_points
        return earned_points

    def calculate_points(self, amount):
        return amount // 1

    def redeem_points(self, points_needed):
        if self.points >= points_needed:
            self.points -= points_needed
            return True
        else:
            return False

@app.route('/add_customer', methods=['POST'])
def add_customer():
    data = request.json
    name = data['name']
    if name not in customers:
        customers[name] = Customer(name)
        return jsonify({"message": f"Customer {name} added."}), 200
    else:
        return jsonify({"error": "Customer already exists."}), 400

@app.route('/purchase', methods=['POST'])
def make_purchase():
    data = request.json
    name = data['name']
    amount = data['amount']
    if name in customers:
        customer = customers[name]
        points = customer.make_purchase(amount)
        return jsonify({"message": f"{points} points earned.", "total_points": customer.points}), 200
    else:
        return jsonify({"error": "Customer not found."}), 404

@app.route('/redeem', methods=['POST'])
def redeem_points():
    data = request.json
    name = data['name']
    points_needed = data['points']
    if name in customers:
        customer = customers[name]
        if customer.redeem_points(points_needed):
            return jsonify({"message": "Points redeemed successfully.", "remaining_points": customer.points}), 200
        else:
            return jsonify({"error": "Not enough points."}), 400
    else:
        return jsonify({"error": "Customer not found."}), 404

@app.route('/points/<name>', methods=['GET'])
def get_points(name):
    if name in customers:
        customer = customers[name]
        return jsonify({"name": name, "points": customer.points}), 200
    else:
        return jsonify({"error": "Customer not found."}), 404

if __name__ == '__main__':
    app.run(debug=True)
