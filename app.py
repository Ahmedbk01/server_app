import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Server ready"

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    number = data.get('number')
    url = f"https://www.hitta.se/sök?vad={number}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        for script_or_style in soup(['script', 'style', 'head', 'footer', 'noscript']):
            script_or_style.decompose()

        result_elements = soup.find_all(class_='spacing__right--sm')

        if result_elements:
            results = []
            for element in result_elements:
                results.append(element.get_text(strip=True))
            return jsonify({"success": True, "text": results})
        else:
            return jsonify({"success": False, "text": "No data found."})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Ensure you're using Render's provided port
    app.run(host='0.0.0.0', port=port, debug=True)  # Bind to all available network interfaces
