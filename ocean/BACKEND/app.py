from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import requests

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "Thanks Google and Regex for the help!"

@app.route('/search', methods=['POST'])
def main():
    data = request.get_json()
    value = data.get('value')
    domain = data.get('domain', '')
    subdomain = data.get('subdomain', '')

    API_KEY = 'AIzaSyDUqjTB9z-GvXdSZ6lKDZwgz0_59gJjOiM'
    CSE_ID = '848d9e0a11f214054'
    query = f"site:linkedin.com/in {domain} {subdomain} AND INDIA"

    google_response = google_search(query, API_KEY, CSE_ID)

    extracted_json = extract(google_response)
    with open('output.json', 'w') as f:
        f.write(extracted_json)  

    return app.response_class(
        response=extracted_json,
        mimetype='application/json'
    )

def google_search(query, API_KEY, CSE_ID):
    url = f"https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": API_KEY,
        "cx": CSE_ID
    }
    res = requests.get(url, params=params)
    if res.status_code == 200:
        print(type(res.json()))  # Should print <class 'dict'>
        return res.json()
    else:
        raise Exception(f"Error: {res.status_code}")

def extract(json_data):
    result = []
    for item in json_data['items']:
        a = item['title'].split('|')[0]
        a = a.split('-')
        entry = {
            "name": a[0].strip(),
            "work_or_location": ''.join([item.strip() for item in a[1:]]),
            "contact": item['link'],
            "about": item['snippet']
        }
        result.append(entry)
    json_result = json.dumps(result, indent=4)
    print(type(json_result))  # Should print <class 'str'>
    return json_result

if __name__ == '__main__':
    app.run(debug=True)