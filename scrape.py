import requests
import bs4
import shutil

IMAGE_URL = "https://www.njlottery.com/content/dam/portal/images/instant-games/0{}/ticket.png"

def grabSite(url):
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	return requests.get(url, headers=headers)

def download_image(idVal):
	url = IMAGE_URL.format(idVal)
	response = requests.get(url, stream=True)
	with open('images/{}.png'.format(idVal), 'wb') as out_file:
	    shutil.copyfileobj(response.raw, out_file)
	del response



if __name__ == '__main__':
	download_image(1529)
