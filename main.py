import requests
import bs4
import json
import os

# REMAINING -

REMAINING = "paidTickets"
TOTAL = "winningTickets"
# Total Winning = TOTAL - REMAINING


def grabSite(url):
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	return requests.get(url, headers=headers)

def download_dataset():
	data = grabSite("https://www.njlottery.com/api/v1/instant-games/games?size=1000&_=1552441310203")
	data = data.json()
	with open('data.json', 'w') as fp:
		json.dump(data, fp, indent=4)

def calc_percent_claimed(val):
	gameName = val['gameName']
	a = []
	for v in val['prizeTiers']:
		prizeAmount = v['prizeDescription']
		percent = (float(v[REMAINING]) / float(v[TOTAL])) * 100
		if v['prizeAmount'] > 50000 and v['winningTickets'] > 1:
			a.append(percent)
			#print("{} | {}% of {} ticket have been won".format(gameName, percent, prizeAmount))
	if len(a) != 0:
		return float(sum(a)) / float(len(a))
	return 0

def calc_total_winning(val):
	gameName = val['gameName']
	a = []
	info = {'game': gameName, 'claimed':0, 'all': 0, 'remaining':0}
	for v in val['prizeTiers']:
		info = {'game': gameName, 'totalClaimed': val["totalTicketsPrinted"], 'claimed':0, 'all': 0, 'remaining':0}
		info['claimed'] += (v[TOTAL] - v[REMAINING]) * v['prizeAmount']
		info['all'] += v[TOTAL] * v['prizeAmount']
		info['remaining'] += v[REMAINING] * v['prizeAmount']
		info['claimed'] = info['claimed'] / 100
		info['all'] = info['all'] / 100
		info['remaining'] = info['remaining'] / 100
		info['percentClaimed'] = (float(info['claimed']) / float(info['all'])) * 100
		e = {'game': gameName, 'prize': v['prizeAmount']/100, 'chance': (float(v[REMAINING]) / float(info['totalClaimed'])) * 100}
		a.append(e)
	return a


def calc_percent_claim(val):
	gameName = val['gameName']
	a = []
	for v in val['prizeTiers']:
		prizeAmount = v['prizeDescription']
		percent = (float(v['paidTickets']) / float(v['winningTickets'])) * 100
		if v['prizeAmount'] > 50000 and v['winningTickets'] > 1:
			a.append(percent)
			#print("{} | {}% of people who win {} Prize Actually claim".format(gameName, percent, prizeAmount))
	return float(sum(a)) / float(len(a))


if __name__ == '__main__':
	#res = grabSite(url)
	#page = bs4.BeautifulSoup(res.text, 'lxml')
	if os.path.exists("data.json") == False:
		download_dataset()
	a = json.load(open("data.json"))
	#calc_percent_claim(a)
	for val in a['games']:
		h = calc_total_winning(val)
		for g in h:
			print("{} - {} - {}".format(g['game'],g['prize'],g['chance']))
