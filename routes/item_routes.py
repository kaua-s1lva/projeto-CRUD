from flask import Blueprint, jsonify, request
from models import Item
from utils import load_data, save_data
from datetime import datetime

item_bp = Blueprint('items', __name__)

@item_bp.route('/items', methods=['GET'])
def get_items():
    data = load_data()
    items = [item for item in data['items'] if not item['excluido']]
    return jsonify({"items": items})

@item_bp.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    data = load_data()
    item_data = next((item for item in data['items'] if item['id'] == item_id), None)
    if item_data:
        return jsonify(item_data)
    else:
        return jsonify({"error": "Item não encontrado"}), 404

@item_bp.route('/items', methods=['POST'])
def add_item():
    data = load_data()
    item_data = request.json

    new_item = Item(**item_data)
    new_item.id = len(data['items']) + 1

    data['items'].append(new_item.to_dict())
    save_data(data)

    return jsonify(new_item.to_dict()), 201

@item_bp.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = load_data()
    item_data = next((item for item in data['items'] if item['id'] == item_id), None)

    if item_data:
        item = Item(**item_data)
        updated_data = request.json
        item.update(updated_data)
        item.historico.append({"acao": "edição", "data_hora": datetime.now().isoformat()})

        item_index = data['items'].index(item_data)
        data['items'][item_index] = item.to_dict()
        save_data(data)
        return jsonify(item.to_dict())
    else:
        return jsonify({"error": "Item não encontrado"}), 404

@item_bp.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    data = load_data()
    item_data = next((item for item in data['items'] if item['id'] == item_id), None)

    if item_data:
        item_data['excluido'] = True
        item_data['historico'].append({"acao": "exclusão", "data_hora": datetime.now().isoformat()})
        save_data(data)
        return '', 204
    else:
        return jsonify({"error": "Item não encontrado"}), 404
