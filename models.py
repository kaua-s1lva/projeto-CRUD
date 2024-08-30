from datetime import datetime

class Item:
    def __init__(self, nome, valor, quantidade, item_especial, ingredientes, excluido=False, id=None, data_emissao=None, historico=None):
        self.id = id
        self.nome = nome
        self.valor = valor
        self.quantidade = quantidade
        self.item_especial = item_especial
        self.ingredientes = ingredientes
        self.excluido = excluido
        self.data_emissao = data_emissao or datetime.now().isoformat()
        self.historico = historico or [{"acao": "criação", "data_hora": self.data_emissao}]

    def update(self, data):
        self.nome = data.get('nome', self.nome)
        self.valor = data.get('valor', self.valor)
        self.quantidade = data.get('quantidade', self.quantidade)
        self.item_especial = data.get('item_especial', self.item_especial)
        self.ingredientes = data.get('ingredientes', self.ingredientes)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'valor': self.valor,
            'quantidade': self.quantidade,
            'item_especial': self.item_especial,
            'ingredientes': self.ingredientes,
            'excluido': self.excluido,
            'data_emissao': self.data_emissao,
            'historico': self.historico
        }
