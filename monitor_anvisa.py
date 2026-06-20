import os
import requests
from datetime import datetime

# CONFIGURAÇÕES
PALAVRAS_CHAVE = ["transporte", "armazenagem", "medicamento", "termolabel", "termolabeis", "rdc"]
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def enviar_alerta_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": mensagem, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

def buscar_atualizacoes_anvisa():
    # Simulando a busca no DOU/ANVISA
    # Dica: O GitHub Actions rodará isso diariamente
    url_api = "https://www.in.gov.br/o/jornal-autentico/pesquisa"
    data_hoje = datetime.now().strftime("%d/%m/%Y")
    params = {"q": "ANVISA RDC", "date": data_hoje}
    
    try:
        response = requests.get(url_api, params=params, timeout=15)
        if response.status_code == 200:
            resultados = response.json().get("materias", [])
            for materia in resultados:
                texto_alvo = (materia.get("titulo", "") + " " + materia.get("ementa", "")).lower()
                
                if any(palavra in texto_alvo for palavra in PALAVRAS_CHAVE):
                    msg = (
                        f"⚠️ *Nova RDC da ANVISA Detectada!*\n\n"
                        f"*Título:* {materia.get('titulo')}\n"
                        f"*Link:* https://www.in.gov.br/web/dou/-/{materia.get('id')}"
                    )
                    enviar_alerta_telegram(msg)
    except Exception as e:
        print(f"Erro na execução: {e}")

if __name__ == "__main__":
    # Linha de teste: o robô vai te mandar isso assim que rodar!
    enviar_alerta_telegram("🚀 *Teste de Conexão:* O monitor da ANVISA está ativo e configurado com sucesso!")
    
    buscar_atualizacoes_anvisa()
