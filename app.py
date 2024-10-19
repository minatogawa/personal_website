from flask import Flask, render_template, url_for
import json
from datetime import datetime, timedelta
import subprocess

app = Flask(__name__)

def load_publications():
    try:
        with open('publications.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        last_updated = datetime.fromisoformat(data['last_updated'])
        if datetime.now() - last_updated > timedelta(days=1):
            subprocess.run(["python", "update_publications.py"])
            with open('publications.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
        
        # Translate column names to English
        publications = []
        for pub in data['publications']:
            publications.append({
                'Title': pub['Título'],
                'Journal': pub['Revista'],
                'Year': pub['Ano'],
                'DOI': pub['DOI'],
                'Citations': int(pub['Citações'])
            })
        
        return publications, data['last_updated']
    except FileNotFoundError:
        subprocess.run(["python", "update_publications.py"])
        with open('publications.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        # Translate column names to English (same as above)
        publications = []
        for pub in data['publications']:
            publications.append({
                'Title': pub['Título'],
                'Journal': pub['Revista'],
                'Year': pub['Ano'],
                'DOI': pub['DOI'],
                'Citations': int(pub['Citações'])
            })
        return publications, data['last_updated']

@app.route('/')
def index():
    publications, last_updated = load_publications()
    return render_template('index.html', publications=publications, last_updated=last_updated)

if __name__ == '__main__':
    app.run(debug=True)
