from flask import Flask, render_template, jsonify, request
import json
from datetime import datetime

app = Flask(__name__)

# Carregar os dados do arquivo JSON
def load_data():
    with open('data.json', 'r') as file:
        return json.load(file)

# Salvar os dados no arquivo JSON
def save_data(data):
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

# Rota para obter todos os itens
@app.route('/items', methods=['GET'])
def get_items():
    data = load_data()
    # Filtrar apenas os itens que não foram excluídos
    items = [item for item in data['items'] if not item.get('excluido', False)]
    return jsonify({"items": items})

# Rota para obter um item específico
@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    data = load_data()
    item = next((item for item in data['items'] if item['id'] == item_id), None)
    if item:
        return jsonify(item)
    else:
        return jsonify({"error": "Item não encontrado"}), 404

# Rota para adicionar um novo item
@app.route('/items', methods=['POST'])
def add_item():
    new_item = request.json
    data = load_data()

    new_item['id'] = len(data['items']) + 1
    new_item['data_emissao'] = datetime.now().isoformat()
    new_item['excluido'] = False  # Novo item não está excluído por padrão
    new_item['historico'] = [{"acao": "criação", "data_hora": datetime.now().isoformat()}]

    data['items'].append(new_item)
    save_data(data)

    return jsonify(new_item), 201

# Rota para atualizar um item existente
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = load_data()
    item = next((item for item in data['items'] if item['id'] == item_id), None)

    if item:
        updated_item = request.json
        item.update(updated_item)
        item['historico'].append({"acao": "edição", "data_hora": datetime.now().isoformat()})
        save_data(data)
        return jsonify(item)
    else:
        return jsonify({"error": "Item não encontrado"}), 404

# Rota para "excluir" um item (marcar como excluído)
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    data = load_data()
    item = next((item for item in data['items'] if item['id'] == item_id), None)

    if item:
        item['excluido'] = True  # Marcar o item como excluído
        item['historico'].append({"acao": "exclusão", "data_hora": datetime.now().isoformat()})
        save_data(data)
        return '', 204
    else:
        return jsonify({"error": "Item não encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True)
