from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import requests

app = Flask(__name__)
CORS(app)

def handle_custom1():
    return [
        {"domain": "AI", "subdomain": "Computer Vision"},
        {"domain": "AI", "subdomain": "NLP"},
        {"domain": "AI", "subdomain": "RL"},
    ]

def handle_custom2():
    return [
        {"domain": "Web", "subdomain": "Vue.js"},
        {"domain": "Web", "subdomain": "React"},
        {"domain": "Web", "subdomain": "Svelte"},
    ]

@app.route('/process', methods=['POST'])
def process_data():
    data = request.get_json()
    mode = data.get('mode')  # key to decide which function to call

    if mode == 'custom1':
        return jsonify(handle_custom1())
    elif mode == 'custom2':
        return jsonify(handle_custom2())
    else:
        # fallback if mode is not provided
        domain = data.get('domain', 'None')
        subdomain = data.get('subdomain', 'None')
        return jsonify([
            {"domain": domain, "subdomain": subdomain}
        ])

if __name__ == '__main__':
    app.run(debug=True)
