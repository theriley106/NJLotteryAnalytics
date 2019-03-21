from flask import Flask, render_template, request, url_for, redirect, Markup, jsonify, make_response, send_from_directory, session
import json
import random
import time

app = Flask(__name__, static_url_path='/static')

db = {}
for val in json.load(open("data.json"))['games']:
	db[val['gameId']] = val

def play_ticket(gameId):
	lotteryNum = random.randint(1, db[gameId]['totalTicketsPrinted'])
	db[gameId]['totalTicketsPrinted'] = db[gameId]['totalTicketsPrinted'] - 1
	response = {"success": True, "winning": False, "info": None, "number": lotteryNum, "time": int(time.time()), "ticketsLeft": db[gameId]['totalTicketsPrinted']}
	prevNum = 0
	for ticketTypes in db[gameId]['prizeTiers']:
		if lotteryNum > prevNum and lotteryNum < (prevNum + ticketTypes['paidTickets']):
			response['winning'] = True
			response['info'] = ticketTypes
			ticketTypes['paidTickets']  = ticketTypes['paidTickets'] - 1
			break
		prevNum += ticketTypes['paidTickets']
	return response


@app.route('/api/<gameId>', methods=['GET'])
def index(gameId):
	return jsonify(play_ticket(gameId))

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000, debug=True)
