from flask import Flask, request, jsonify
from flask_cors import CORS
import json, requests, dotenv, os, time
from dotenv import load_dotenv
from google import genai
from google.genai import types

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "Thanks Google and Regex for the help!"

@app.route('/search', methods=['POST'])
def main():
    dotenv.load_dotenv()
    SEARCH_API = os.getenv('SEARCH_KEY')
    SEARCH_ID = os.getenv('SEARCH_ID')
    GEMMA_API = os.getenv('GEMMA_KEY')
    client = genai.Client(api_key=GEMMA_API)
    data = request.get_json()
    value = data.get('value')
    domain = data.get('domain', '')
    subdomain = data.get('subdomain', '')
    query = f"site:linkedin.com/in {domain} {subdomain} AND INDIA"

    google_response = google_search(query, SEARCH_API, SEARCH_ID)
    if google_response:
        print('Google response successfully received.')
    with open('gpse_response.json', 'w') as f:
        f.write(json.dumps(google_response, indent=4))

    extracted_json = extract(google_response, domain, subdomain, client)
    if extracted_json:
        print('Extraction successfully completed.')
    with open('extracted.json', 'w') as f:
        f.write(extracted_json)  

    return app.response_class(
        response=extracted_json,
        mimetype='application/json'
    )

def google_search(query, SEARCH_API, SEARCH_ID):
    url = f"https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": SEARCH_API,
        "cx": SEARCH_ID
    }
    res = requests.get(url, params=params)
    if res.status_code == 200:
        return res.json()
    else:
        raise Exception(f"Error: {res.status_code}")

def extract(json_data, domain, subdomain, client):
    result = []
    for item in json_data['items']:
        a = item['title'].split('|')[0]
        a = a.split('-')
        score = item['snippet']
        response = client.models.generate_content(
            model="gemma-3n-e4b-it",
            contents = f"Confidence score (65-100) for bio: {score} in {domain} {subdomain.strip()}. Reply with number only.",
            config=types.GenerateContentConfig(
                max_output_tokens=2,
            )
        )
        entry = {
            "name": a[0].strip(),
            "work_or_location": ''.join([item.strip() for item in a[1:]]),
            "contact": item['link'],
            "confidence_score": response.text
        }
        result.append(entry)
        time.sleep(1)

    json_result = json.dumps(result, indent=4)
    return json_result

if __name__ == '__main__':
    app.run(debug=True)