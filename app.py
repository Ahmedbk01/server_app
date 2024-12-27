from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)  # Enable CORS for the entire app

@app.route('/')
def home():
    return "Server ready"  # This will display "Server ready" when you open the link in a browser.


@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    number = data.get('number')
    url = f"https://www.hitta.se/sök?vad={number}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        # Send GET request to the URL
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Ensure request was successful
        
        # Parse the page with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove unwanted tags like script and style
        for script_or_style in soup(['script', 'style', 'head', 'footer', 'noscript']):
            script_or_style.decompose()  # Remove the tag from the tree

        # Find all elements with the class 'spacing__right--sm' (you can adjust this if needed)
        result_elements = soup.find_all(class_='spacing__right--sm')

        # Check if results are found
        if result_elements:
            results = []
            for element in result_elements:
                # Extract the text content and add it to the results list
                results.append(element.get_text(strip=True))
            
            return jsonify({"success": True, "text": results})
        else:
            return jsonify({"success": False, "text": "No data found."})
    
    except Exception as e:
        # Handle any errors during the scraping process
        print(f"Error: {e}")
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)