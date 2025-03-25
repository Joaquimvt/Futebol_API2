from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)

API_KEY = "ccfd023e4acd44e29e8ab4dc5b49bc68"
BASE_URL = "https://api.football-data.org/v4/competitions/PL"
HEADERS = {"X-Auth-Token": API_KEY}

# Função para filtrar partidas de 2025
# def filtrar_partidas_2025(partidas):
def filtrar_partidas_2025(partidas):
    # Verifica se a chave "matches" existe e se é uma lista
    if "matches" in partidas and isinstance(partidas["matches"], list):
        return [match for match in partidas["matches"] if "2025" in match.get("utcDate", "")]
    return []  # Retorna uma lista vazia se a chave não existir ou não for uma lista

# Página inicial com dados atualizados
@app.route("/")
def home():
    classificacao_url = f"{BASE_URL}/standings"
    partidas_url = f"{BASE_URL}/matches"
    artilheiros_url = f"{BASE_URL}/scorers"
    
    classificacao = requests.get(classificacao_url, headers=HEADERS).json()
    partidas = requests.get(partidas_url, headers=HEADERS).json()
    artilheiros = requests.get(artilheiros_url, headers=HEADERS).json()
    
    partidas_2025 = filtrar_partidas_2025(partidas)
    
    return render_template("index.html", classificacao=classificacao, partidas={"matches": partidas_2025}, artilheiros=artilheiros)

# Endpoint para partidas de 2025
@app.route("/partidas", methods=["GET"])
def get_partidas():
    url = f"{BASE_URL}/matches"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        partidas = response.json()
        partidas_2025 = filtrar_partidas_2025(partidas)
        return jsonify({"matches": partidas_2025})
    return jsonify({"error": "Erro ao buscar dados"}), 500

if __name__ == "__main__":
    app.run(debug=True)
