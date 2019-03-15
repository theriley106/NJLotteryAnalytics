import requests
import bs4
import json
import os


def grabSite(url):
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	return requests.get(url, headers=headers)

def download_dataset():
	data = grabSite("https://www.njlottery.com/api/v1/instant-games/games?size=1000&_=1552441310203")
	data = data.json()
	with open('data.json', 'w') as fp:
		json.dump(data, fp, indent=4)

if __name__ == '__main__':
	#res = grabSite(url)
	#page = bs4.BeautifulSoup(res.text, 'lxml')
	if os.path.exists("data.json") == False:
		download_dataset()
	a = json.load(open("data.json"))
	for val in a['games']:
		gameName = val['gameName']
		for v in val['prizeTiers']:
			prizeAmount = v['prizeDescription']
			percent = (float(v['paidTickets']) / float(v['winningTickets'])) * 100
			if v['prizeAmount'] > 50000 and v['winningTickets'] > 1:
				print("{}% of people who win {} Prize Actually claim for {}".format(percent, prizeAmount, gameName))


