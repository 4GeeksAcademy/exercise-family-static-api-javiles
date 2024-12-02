"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import APIException, generate_sitemap

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)


class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name
        self.members = [
            {'first_name': 'John', 'age': 33, 'id': 1, 'lucky_numbers': [7, 13, 22] },
            {'first_name': 'Jane','age': 35, 'id': 2, 'lucky_numbers': [10, 14, 3]},
            {'first_name': 'Jimmy', 'age': 5, 'id': 3, 'lucky_numbers': [1]}
        ]

    def get_all_members(self):
        return self.members

    def get_member(self, member_id):
        for member in self.members:
            if member["id"] == member_id:
                return member
        return None

    def delete_member(self, member_id):
        for index, member in enumerate(self.members):
            if member["id"] == member_id:
                del self.members[index]
                return True
        return False

    def add_member(self, member):
        self.members.append(member)

    def generate_id(self):
        existing_ids = [member["id"] for member in self.members]
        return max(existing_ids) + 1 if existing_ids else 1


jackson_family = FamilyStructure("Jackson")


@app.route('/members', methods=['GET'])
def get_all_members():
    return jsonify(jackson_family.get_all_members()), 200


@app.route('/member', methods=['POST'])
def add_a_new_member():
    member = request.get_json()

    if not all(key in member for key in ("first_name", "age", "lucky_numbers")):
        return jsonify({"error": "Invalid member data"}), 400

    member["id"] = member.get("id", jackson_family.generate_id())

    jackson_family.add_member(member)
    return jsonify(member), 200

@app.route('/member/<int:id>', methods=['GET'])
def get_member_by_id(id):
    member = jackson_family.get_member(id)
    if not member:
        return jsonify({"error": "Member not found"}), 404

    return jsonify({
        "first_name": member["first_name"],
        "id": member["id"],
        "age": member["age"],
        "lucky_numbers": member["lucky_numbers"]
    }), 200


@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):
    success = jackson_family.delete_member(id)
    if not success:
        return jsonify({"error": "Member not found"}), 404
    return jsonify({"done": True}), 200


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)