import requests
import googlemaps
import urllib
import re
import urllib.request, json 

from lxml import html
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime

########

def gethtml(url, path, subpath):
	page = requests.get(url)
	html_str = html.fromstring(page.text)
	html_elements =  html_str.xpath(path)
	print(len(html_elements))
	yield html_elements
	url = html_str.xpath(subpath)
	print(url[0])
	if (url != None):		
		gethtml(url[0], path, subpath )
	else:
		print("None url")

def get_distance(curr_location, dest):
	gkey = 'AIzaSyBa2Cii0GnxCs6zE1M-KsmQb4eSwmwe84E'
	googlehttp = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins='\
					 + curr_location + '&destinations=' + dest +'&key=' + gkey
	# print(googlehttp)
	res = requests.get(googlehttp)
	distance = res.json()['rows'][0]['elements'][0]
	if 'distance' in distance:
		return distance['distance']['value']
	else:
		return None

def get_info(location, root_url, detail_url_xpath, info_xpath):
	lists = []

	page = requests.get(root_url)
	html_str = html.fromstring(page.text)
	list_links = html_str.xpath(detail_url_xpath)
	pprint(list_links)
	for i in range(len(list_links)):	
		if list_links[i].startswith('/thuong-hieu'):
			link_xp = "//div[@class='ldc-item-h-name']/h2/a//@href"
			get_info(location, "https://foody.vn" + list_links[i], link_xp, info_xpath)
		else:
			detail_page = requests.get("https://foody.vn" + list_links[i])
			detail_html = html.fromstring(detail_page.text)
			info_lists = {}
			for key in info_xpath:
				result = detail_html.xpath(info_xpath[key])
				info_lists[key] = result[0]
			info_lists['distance'] = get_distance(location, convert(info_lists['street']) + ',' + convert(info_lists['district']) )
			lists.append(info_lists)
	print("asasassa" ,len(list(lists)[0]))
	pprint(list(lists))
	yield list(lists)


patterns = {
    '[àáảãạăắằẵặẳâầấậẫẩ]': 'a',
    '[đ]': 'd',
    '[èéẻẽẹêềếểễệ]': 'e',
    '[ìíỉĩị]': 'i',
    '[òóỏõọôồốổỗộơờớởỡợ]': 'o',
    '[ùúủũụưừứửữự]': 'u',
    '[ỳýỷỹỵ]': 'y'
}

def convert(text):
    output = text
    for regex, replace in patterns.items():
        output = re.sub(regex, replace, output)
        output = re.sub(regex.upper(), replace.upper(), output)
    return output

if __name__ == "__main__":

	# url = 'http://www.clingme.vn/Deal/Search?keySearch=ga%20quay&streetName=&distance=20&sortby=1&option=2'
	# detail_link = "//div[@class='tile-add-deal']/a[@class='title-deal text-left']//@href"
	# info = {}
	# info['location'] = "//p[@class='p-address clearfix']//text()"
	# info['name'] = "//h1[@class='detail-title text-left']//text()"



	url = 'https://www.foody.vn/ha-noi/dia-diem?q=ga+ran+&ss=header_search_form'
	detail_link = "//div[@class='resname']/h2/a//@href"
	info = {}
	info['name'] = "//h1[@itemprop='name']//text()"
	info['street'] = "//span[@itemprop='streetAddress']//text()"
	info['district'] = "//span[@itemprop='addressLocality']//text()"
	lists = get_info('133 Xuan Thuy', url, detail_link, info)
	pprint(list(lists)[0])