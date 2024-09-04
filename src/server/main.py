from flask import Flask, jsonify, request  # type: ignore
from waitress import serve  # type: ignore
from scrape import Scrape  # type: ignore

app = Flask(__name__)

scraper = Scrape()

@app.route('/snipe', methods=['POST'])
def collection_and_tx():
    try:
        data = request.get_json()
        scraper.state['collection_name'] = data["collection_name"]
        scraper.state['user_pubkey'] = data["user_pubkey"]
        
        data = scraper.scrape_and_construct()
        
        return jsonify({"data": data})
    except KeyError as e:
        return jsonify({"error": f"Missing key: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/collection_tokens', methods=['POST'])
def get_listed_tokens():
    try:
        data = request.get_json()
        scraper.state['collection_name'] = data["collection_name"]
        data = scraper.get_listed_tokens()
        
        return jsonify(data)
    except KeyError as e:
        return jsonify({"error": f"Missing key: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/candy_machines', methods=['GET'])
def get_candy_machines():
    try:
        data = scraper.get_candy_machines()
        
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=3000)