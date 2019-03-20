from flask import Flask, render_template, request, url_for, redirect, Markup, jsonify, make_response, send_from_directory, session
import json

app = Flask(__name__, static_url_path='/static')

db = {}
for val in json.load(open("data.json"))['games']:
	db[val['gameId']] = val

@app.route('/', methods=['GET'])
def index():
	return render_template("index.html")

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)
