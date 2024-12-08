# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from flask_cors import CORS
from data import embalagens, medicamentos

app = Flask(__name__)
CORS(app)

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    produtos = data.get("produtos")  # Lista de produtos: [{"medicamento": "Paracetamol", "quantidade": 10}, ...]

    if not produtos:
        return jsonify({"error": "Nenhum produto selecionado."}), 400

    # Separar medicamentos por tipo
    tipos = {"normal": [], "controlado": [], "perfumaria": []}
    for item in produtos:
        medicamento = item.get("medicamento")
        quantidade = item.get("quantidade")

        if medicamento not in medicamentos:
            return jsonify({"error": f"Medicamento invalido: {medicamento}"}), 400

        med_info = medicamentos[medicamento]
        tipo = med_info["tipo"]
        tipos[tipo].append({"medicamento": medicamento, "quantidade": quantidade, "volume": med_info["largura"] * med_info["altura"] * med_info["profundidade"]})

    resultado_final = {}

    for tipo, itens in tipos.items():
        if not itens:
            continue

        # Calcular o volume total do tipo
        total_volume = sum(item["volume"] * item["quantidade"] for item in itens)

        # Ordenar embalagens por tamanho decrescente
        sorted_embalagens = sorted(embalagens.items(), key=lambda x: x[1]["largura"] * x[1]["altura"] * x[1]["profundidade"], reverse=True)

        distribuicao = []
        volumes_embalagens = [emb[1]["largura"] * emb[1]["altura"] * emb[1]["profundidade"] for emb in sorted_embalagens]
        nomes_embalagens = [emb[0] for emb in sorted_embalagens]

        # Encontrar a combinação de embalagens
        restante_volume = total_volume
        while restante_volume > 0:
            for i, vol_emb in enumerate(volumes_embalagens):
                if restante_volume >= vol_emb or (i == len(volumes_embalagens) - 1):  # Força o uso da menor embalagem quando necessário
                    capacidade_restante = vol_emb
                    itens_na_embalagem = {}

                    for item in itens:
                        if item["quantidade"] == 0:
                            continue

                        volume_item = item["volume"]
                        max_cabem = capacidade_restante // volume_item
                        quantidade_a_inserir = min(item["quantidade"], max_cabem)

                        if quantidade_a_inserir > 0:
                            itens_na_embalagem[item["medicamento"]] = quantidade_a_inserir
                            item["quantidade"] -= quantidade_a_inserir
                            capacidade_restante -= quantidade_a_inserir * volume_item

                    distribuicao.append({"embalagem": nomes_embalagens[i], "itens": itens_na_embalagem})
                    restante_volume -= vol_emb
                    break

        resultado_final[tipo] = {
            "distribuicao": distribuicao,
        }

    return jsonify(resultado_final)

if __name__ == "__main__":
    app.run(debug=True)
