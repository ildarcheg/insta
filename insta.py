import sys
from lxml import etree
from io import StringIO, BytesIO
import os.path
import urllib
import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import time

url = 'https://www.instagram.com/graphql/query/?query_hash=56066f031e6239f35a904ac20c9f37d9&variables=%7B%22id%22%3A%221555589847%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Afalse%2C%22first%22%3A12%2C%22after%22%3A%22QVFDSG5NWEdYOEVLamZjampjc2s4NUg2OEJMb2hXUjNNX0J3ejdxdjFvZmx3ajhuR0NLbEl2Q3lCRVozMzU2cWIwZnlIeVdhdVBrYjlzcXphWUVab25qeQ%3D%3D%22%7D'
un_url = urllib.unquote(url)
print(un_url)
main_url = 'https://www.instagram.com/graphql/query/?query_hash='
var_s = '&variables='
un_url = un_url.replace(main_url, '')
id_s, param_s = un_url.split(var_s)
print(id_s)
print(param_s)

main_url = 'https://www.instagram.com/graphql/query/?query_hash='
var_s = '&variables='
query_hash = '56066f031e6239f35a904ac20c9f37d9'
params = '{"id":"1555589847","include_reel":true,"fetch_mutual":false,"first":12,"after":"QVFDSG5NWEdYOEVLamZjampjc2s4NUg2OEJMb2hXUjNNX0J3ejdxdjFvZmx3ajhuR0NLbEl2Q3lCRVozMzU2cWIwZnlIeVdhdVBrYjlzcXphWUVab25qeQ=="}'
new_url = main_url+query_hash+var_s+urllib.quote(params)
page_json = json.loads(tree.xpath("//body/pre")[0].text)
json.loads(tree.xpath("//text()")[0])

def getWebdriver():
	WINDOW_SIZE = "1920,1080"
	prefs = {"profile.managed_default_content_settings.images": 2}
	chrome_options = Options()  
	chrome_options.add_experimental_option("prefs", prefs)
	#chrome_options.add_argument("--headless")  
	#chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
	return webdriver.Chrome(chrome_options=chrome_options) 


# START
# open insta and log in
base_link = 'https://www.instagram.com'
driver = webdriver.Chrome() 
driver.get(base_link+'/accounts/login/?hl=en')
uname = driver.find_element_by_name("username")
uname.send_keys('ildarcheg.developer@gmail.com')
passw = driver.find_element_by_name("password")
passw.send_keys('ghtdtl111')
button = driver.find_elements_by_xpath("//button[.//text()='Log in']")[0]
button.click()

# get user page
target_url = base_link+'/mayoucai656/'
driver.get(target_url)
page_source = driver.page_source

# get user id and hash id
user_id = str(re.findall(r'profilePage_(\d+)', page_source)[0])
consumer_script_link = base_link + str(re.findall(r'/static/bundles/metro/Consumer\.js/[A-Za-z0-9]{5,13}\.js', page_source)[0])
driver.get(consumer_script_link)
page_source = driver.page_source
parser = etree.HTMLParser()
tree = etree.parse(StringIO(page_source), parser)
script_source = tree.xpath("//body/pre")[0].text
hash_id = str(re.findall(r';var n="([A-Za-z0-9]{30,34})",', script_source)[0])

# login again
driver.get(base_link+'/accounts/login/?hl=en')
uname = driver.find_element_by_name("username")
uname.send_keys('ildarcheg.developer@gmail.com')
passw = driver.find_element_by_name("password")
passw.send_keys('ghtdtl111')
button = driver.find_elements_by_xpath("//button[.//text()='Log in']")[0]
button.click()

time.sleep(3)

# prepare request link
first_link = '{' + '"id":"{user_id}","include_reel":true,"fetch_mutual":true,"first":24'.format(user_id=user_id) + '}'
first_link_encoded = urllib.quote(first_link)
link = base_link + '/graphql/query/?query_hash=' + hash_id + '&variables=' + first_link_encoded

def get_info(link, num):
	driver.get(link)
	page_source = driver.page_source
	# parse json
	parser = etree.HTMLParser()
	tree = etree.parse(StringIO(page_source), parser)
	json_source = tree.xpath("//body/pre")[0].text
	json_response = json.loads(str(json_source))
	has_next_page = json_response[u'data'][u'user'][u'edge_followed_by'][u'page_info'][u'has_next_page']
	end_cursor = str(json_response[u'data'][u'user'][u'edge_followed_by'][u'page_info'][u'end_cursor'])
	link = '{' + '"id":"{user_id}","include_reel":true,"fetch_mutual":false,"first":{num},"after":"{end_cursor}"'.format(user_id=user_id, num=num, end_cursor=end_cursor) +'}'
	link_encoded = urllib.quote(link)
	final_link = base_link + '/graphql/query/?query_hash=' + hash_id + '&variables=' + link_encoded
	return {'has_next_page':has_next_page, 'end_cursor':end_cursor, 'final_link':final_link, 'edges':json_response[u'data'][u'user'][u'edge_followed_by'][u'edges']}

edges = []
x = get_info(link, 12)
got_total_nodes = 0
edges.extend(x['edges'])
got_total_nodes = len(edges)
print('nodes: ', got_total_nodes)
while x['has_next_page']:
	x = get_info(x['final_link'], 12)
	edges.extend(x['edges'])
	got_total_nodes = len(edges)
	print('nodes: ', got_total_nodes)
	print(x['has_next_page'])
	time.sleep(1)


driver.get(final_link)
page_source = driver.page_source

# ;var n="56066f031e6239f35a904ac20c9f37d9",o


#<script type="text/javascript" src="/static/bundles/metro/Consumer.js/d4d78c384d06.js" crossorigin="anonymous"></script>
#;var n="[A-Za-z0-9]{30,34}",

submit_button = driver.find_element_by_class_name("sendbutton").click()
driver.find_elements_by_xpath("//*[contains(text(), 'Log in')]").click()
print(new_url)

https://www.instagram.com/graphql/query/?query_hash=56066f031e6239f35a904ac20c9f37d9&variables={"id":"1555589847","include_reel":true,"fetch_mutual":false,"first":12,"after":"QVFDSG5NWEdYOEVLamZjampjc2s4NUg2OEJMb2hXUjNNX0J3ejdxdjFvZmx3ajhuR0NLbEl2Q3lCRVozMzU2cWIwZnlIeVdhdVBrYjlzcXphWUVab25qeQ=="}


class User(object):
	def __init__(self, userID = '', itemsID = []):
		self.id = userID
		self.itemsID = itemsID
	def getString(self):
		return ''+str(self.id)+'\t'+','.join(str(x) for x in self.itemsID) 

class UsersCollection(object):
	def __init__(self):
		self.users = []
		self.usersID = []
		self.itemsID = []
		self.fileuser = 'user.csv'
		self.fileitems = 'items.csv'
	def addUser(self, user):
		if user.id not in self.usersID and user not in self.users:
			self.users.append(user)
			self.usersID.append(user.id)
	def addItemID(self, itemID):
		if itemID not in self.itemsID:
			self.itemsID.append(itemID)
	def existsUserID(self, userID):
		return userID in self.usersID
	def existsItemID(self, itemID):
		return itemID in self.itemsID
	def getAllItemsID(self):
		itemsID = []
		for user in self.users:
			itemsID.extend(user.itemsID)	
		return list(set(itemsID))
	def getAllItemsIDLess(self):
		itemsID = []
		for user in self.users:
			if len(user.itemsID)>100:
				continue
			itemsID.extend(user.itemsID)	
		return list(set(itemsID))
	def saveToDisk(self):
		with open(self.fileuser, 'w') as f:
			xxx = [x.getString() for x in self.users]
			f.write('\n'.join(xxx))
		with open(self.fileitems, 'w') as f:
			f.write('\n'.join(self.itemsID))
	def loadFromDisk(self):
		if os.path.isfile(self.fileuser): 
			with open(self.fileuser, 'r') as f:
				for line in f:
					userID, itemsID = line.split('\t')
					itemsID = itemsID.strip()
					itemsID = itemsID.split(',')
					self.addUser(User(userID, itemsID))
		if os.path.isfile(self.fileitems): 
			with open(self.fileitems, 'r') as f:
				itemsID = []
				for line in f:
					itemsID.append(line.strip())
				self.itemsID = itemsID

class Downloader(object):
	def __init__(self):
		self.driver = self.getWebdriver()
		self.counter = 0	
	def __del__(self):
		self.driver.close()
	def getSourcePage(self, url, place=''):
		self.counter += 1
		print('--')
		print('C: ', self.counter)
		print(place, url)
		if self.counter > 11:
			self.driver.close()
			self.driver = self.getWebdriver()
			self.counter = 0
			print('---- counter reset ----')
		self.driver.get(url)
		self.driver.get_screenshot_as_file("last_page.png")
		return self.driver.page_source
	def getWebdriver(self):
		WINDOW_SIZE = "1920,1080"
		prefs = {"profile.managed_default_content_settings.images": 2}
		chrome_options = Options()  
		chrome_options.add_experimental_option("prefs", prefs)
		#chrome_options.add_argument("--headless")  
		#chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
		return webdriver.Chrome(chrome_options=chrome_options) 	

def getAllReviewsLinkByItemID(itemID):
	base_link = 'https://www.amazon.com/gp/product/'
	temp_link = base_link + itemID
	page_source = downloader.getSourcePage(temp_link, 'getAllReviewsLinkByItemID')
	tree = etree.parse(StringIO(page_source), parser)
	els = tree.xpath("//a[@data-hook='see-all-reviews-link-foot']")
	if len(els) == 0:
		return None
	else:
		return els[0].attrib['href']

def getAllUsersOnReviewPage(review_link):
	base_link = 'https://www.amazon.com'
	temp_link = base_link + review_link
	page_source = downloader.getSourcePage(temp_link, 'getAllUsersOnReviewPage')
	tree = etree.parse(StringIO(page_source), parser)
	els = tree.xpath("//a[@class='a-profile']")
	usersOnPage = []
	for i in els:
		usersOnPage.append(i.attrib['href'].split('/')[3])
	return usersOnPage

def getItemsByUserID(userID):
	nextPageToken = ''
	itemsID = []
	while nextPageToken != None:
		nextPageToken = nextPageToken.encode('ascii', 'ignore')
		url = 'https://www.amazon.com/profilewidget/timeline/visitor?nextPageToken={}&filteredContributionTypes=productreview&directedId={}'.format(urllib.quote(nextPageToken), userID)
		page_source = downloader.getSourcePage(url, 'getItemsByUserID')
		tree = etree.parse(StringIO(page_source), parser)
		#print('JSON: ', tree.xpath("//text()")[0])
		response_dict = json.loads(tree.xpath("//text()")[0])
		contributions = response_dict['contributions']
		nextPageToken = response_dict['nextPageToken']
		itemsIDOnPage = [i[u'product'][u'asin'].encode('ascii', 'ignore') for i in contributions]
		itemsID.extend(itemsIDOnPage)
	return itemsID

def getUsersIDForItemID(itemID):
	print('itemID: ', itemID)
	review_link_general = getAllReviewsLinkByItemID(itemID)
	if review_link_general is None:
		return []
	base_link = 'https://www.amazon.com'
	print('itemID all reviews page: ', base_link+review_link_general)
	page_source = downloader.getSourcePage(base_link+review_link_general, 'getUsersIDForItemID')
	tree = etree.parse(StringIO(page_source), parser)
	els = tree.xpath("//li[@data-reftag='cm_cr_arp_d_paging_btm']/a/text()")
	if len(els)> 1:
		total_pages = int(els[len(els)-1])
	else:
		total_pages = 1
	if total_pages>10:
		return []
	review_links = []
	to_be_replaced = 'ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews'
	for i in range(0, total_pages):
		replace_end = 'ref=cm_cr_arp_d_paging_btm_{}?ie=UTF8&reviewerType=all_reviews&pageNumber={}'.format(i+1,i+1)
		new_review_link = review_link_general.replace(to_be_replaced, replace_end)
		review_links.append(new_review_link)
	usersForItemID = []
	for review_link in review_links:
		usersForItemIDOnPage = getAllUsersOnReviewPage(review_link)
		usersForItemID.extend(usersForItemIDOnPage)
	return usersForItemID

ids='B07G8DLK1L,B00CKJG7NS,B07JQGNC39,B07J6Q2BPF,B01MZYT1SY,\
		B07GRRZ24K,B07GJ42DB2,B07HH5YV6K,B0713RDBL2,B07GQTRRFL,\
		B0777KZBVJ,B07G7F3CTB,B07H7NQR85,B07H7NQR85,B07HZ1DLHM,\
		B07G45PP87,B07FCQ6N8T,B07JD39DBM,B07F6HDYP5,B07DHSJB9C,\
		B07CZ1THSR,B07HFGXS1H,B07D57KLHK,B07HNJRW4S,B07G34H99N,\
		B07F9M89PY,B06XVMBJHS,B073CMZD1K,B07FS1DKJR,B07BVSZK4Z,\
		B0727YVQQ6,B07FK5HM8K,B0765D1SH9,B07F785JCV,B07CB3ZFWZ,\
		B07DJYH54N,B07HBDC5DS,B07DVZJB3D,B07CV4DNBT,B07BJFTH64,\
		B07B4HKLFK,B01LK0HQDW,B07FTNCB8C,B0777JD5DD,B01M9BFLVR,\
		B07FTVV16D,B07DR5BGR8,B07DWZPY23,B07FT36B8D,B07FSLHW1N,\
		B07DPNB6T5,B0798XT6JJ,B000Y1BGN0,B07FVSHQD7,B07FS1DKJR,\
		B075HJ8L9Z,B07D29TW3Z,B07F2NN6TM,B07G2SPZ6G,B076CK9F7P,\
		B07D7ZV9J9,B07GFVDSJX,B07HJYN8P3,B0753YMRCL,B07DJYH54N,\
		B07D7H5VKF,B071HW7WGS,B00TEPN5TA,B01FWIFRL6,B06Y1WYHZM,\
		B07J6FW99S,B00WSE81K2,B07HPCC5FS,B07H7PH33T,B07HXTCGQG,\
		B07JW4Y67L,B07JFW8YSP,B07JF2DSL5,B07G7F3CTB,B07CH81RGS,\
		B07FCQQXFL,B07JBC7YMY,B07G3JN3S4,B01MD2D7ZG,B07DX3BW39,\
		B079GCQN65,B07HKW2BS8'
ids = ids.replace('\t','').split(",")

user1 = User('amzn1.account.AGKWBHVKAXOGUB4X5BT2ZV2SJPZQ', ids)

parser = etree.HTMLParser()
downloader = Downloader()
col = UsersCollection()
col.loadFromDisk()
#col.add(user1)
# 'B07J6Q2BPF' usersID = getUsersIDForItemID('B07J6Q2BPF')
itemsToCheck = col.getAllItemsID()
for itemID in itemsToCheck:
	if col.existsItemID(itemID):
		print('         ------- ITEM {} exists -------'.format(itemID))
		continue
	usersID = getUsersIDForItemID(itemID)
	users = []
	for userID in usersID:
		if col.existsUserID(userID):
			print('         ------- users {} exists -------'.format(userID))
			continue
		print('----------------------')
		print('----------------------')
		print('----------------------')
		print('itemID:', itemID, 'userID', userID)
		print('----')
		itemsID = getItemsByUserID(userID)
		col.addUser(User(userID, itemsID))
		col.saveToDisk()
	col.addItemID(itemID)
	col.saveToDisk()



# # ref=cm_cr_arp_d_paging_btm_1?ie=UTF8&reviewerType=all_reviews&pageNumber=1
# # '/Whiskey-Glass-Fashioned-Cocktail-Glassware/product-reviews/B01MD2D7ZG/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews'
# # '/Whiskey-Glass-Fashioned-Cocktail-Glassware/product-reviews/B01MD2D7ZG/ref=cm_cr_arp_d_paging_btm_3?ie=UTF8&reviewerType=all_reviews&pageNumber=3'
# # '/Whiskey-Glass-Fashioned-Cocktail-Glassware/product-reviews/B01MD2D7ZG/ref=cm_cr_arp_d_paging_btm_1?ie=UTF8&reviewerType=all_reviews&pageNumber=1'
# # ['/Whiskey-Glass-Fashioned-Cocktail-Glassware/product-reviews/B01MD2D7ZG/ref=cm_cr_arp_d_paging_btm_1?ie=UTF8&reviewerType=all_reviews&pageNumber=1', '/Whiskey-Glass-Fashioned-Cocktail-Glassware/product-reviews/B01MD2D7ZG/ref=cm_cr_arp_d_paging_btm_2?ie=UTF8&reviewerType=all_reviews&pageNumber=2', '/Whiskey-Glass-Fashioned-Cocktail-Glassware/product-reviews/B01MD2D7ZG/ref=cm_cr_arp_d_paging_btm_3?ie=UTF8&reviewerType=all_reviews&pageNumber=3', '/Whiskey-Glass-Fashioned-Cocktail-Glassware/product-reviews/B01MD2D7ZG/ref=cm_cr_arp_d_paging_btm_4?ie=UTF8&reviewerType=all_reviews&pageNumber=4', '/Whiskey-Glass-Fashioned-Cocktail-Glassware/product-reviews/B01MD2D7ZG/ref=cm_cr_arp_d_paging_btm_5?ie=UTF8&reviewerType=all_reviews&pageNumber=5', '/Whiskey-Glass-Fashioned-Cocktail-Glassware/product-reviews/B01MD2D7ZG/ref=cm_cr_arp_d_paging_btm_6?ie=UTF8&reviewerType=all_reviews&pageNumber=6', '/Whiskey-Glass-Fashioned-Cocktail-Glassware/product-reviews/B01MD2D7ZG/ref=cm_cr_arp_d_paging_btm_7?ie=UTF8&reviewerType=all_reviews&pageNumber=7']
# # rev_link = 'https://www.amazon.com/Whiskey-Glass-Fashioned-Cocktail-Glassware/product-reviews/B01MD2D7ZG/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews'

# r = requests.get(url = URL, params = PARAMS) 
# r
# # extracting data in json format 
# data = r.json() 

# URL = 'https://www.amazon.com/profilewidget/timeline/visitor?nextPageToken=&filteredContributionTypes=productreview%2Cglimpse%2Cideas&directedId=amzn1.account.AEBELQXS2ALPK5SW7QXNM56VRDOQ'


# getItemsByUserID('amzn1.account.AEBELQXS2ALPK5SW7QXNM56VRDOQ')


# nextPageToken = response['nextPageToken'].encode('ascii', 'ignore')
# PARAMS = {'nextPageToken':nextPageToken, 'filteredContributionTypes':'productreview', 'directedId':userID}
# r = requests.get(url = URL, headers = headers, params = PARAMS) 
# response = json.loads(r.text)
# print(response['nextPageToken'].encode('ascii', 'ignore'))
# print('contributions: ', len(response['contributions']))
# 	# HTTP REQUETS
# 	# URL = 'https://www.amazon.com/profilewidget/timeline/visitor'
# 	# headers = {'authority': 'www.amazon.com',
# 	# 			'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
# 	# 			'accept-encoding':'gzip, deflate, br',
# 	# 			'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
# 	# 			}
# 	# nextPageToken = ''
# 	# itemsID = []
# 	# while nextPageToken != None:
# 	# 	nextPageToken = nextPageToken.encode('ascii', 'ignore')
# 	# 	PARAMS = {'nextPageToken':nextPageToken, 'filteredContributionTypes':'productreview', 'directedId':userID}
# 	# 	response = requests.get(url = URL, headers = headers, params = PARAMS) 
# 	# 	print('url: ', response.request.url)
# 	# 	print('status: ', response.status_code)
# 	# 	if response.status_code !=200:
# 	# 		nextPageToken=None
# 	# 		continue	
# 	# 	response_dict = json.loads(response.text)
# 	# 	contributions = response_dict['contributions']
# 	# 	nextPageToken = response_dict['nextPageToken']
# 	# 	itemsIDOnPage = [i[u'product'][u'asin'].encode('ascii', 'ignore') for i in contributions]
# 	# 	itemsID.extend(itemsIDOnPage)
# 	# return itemsID