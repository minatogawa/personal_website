import requests
import json
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("SCOPUS_API_KEY")
AUTHOR_ID = "57194039106"

def update_publications():
    url = f"https://api.elsevier.com/content/search/scopus?query=AU-ID({AUTHOR_ID})"
    headers = {
        "X-ELS-APIKey": API_KEY,
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        publications_list = []

        for pub in data['search-results']['entry']:
            publications_list.append({
                'Título': pub.get('dc:title', 'N/A'),
                'Revista': pub.get('prism:publicationName', 'N/A'),
                'Ano': pub.get('prism:coverDate', 'N/A').split("-")[0],
                'DOI': pub.get('prism:doi', 'N/A'),
                'Citações': pub.get('citedby-count', 'N/A')
            })

        with open('publications.json', 'w', encoding='utf-8') as f:
            json.dump({
                'last_updated': datetime.now().isoformat(),
                'publications': publications_list
            }, f, ensure_ascii=False, indent=2)

        print("Publicações atualizadas com sucesso.")
    else:
        print(f"Erro ao atualizar publicações: {response.status_code}")

if __name__ == "__main__":
    update_publications()