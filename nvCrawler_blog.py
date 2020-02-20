import os
import csv
import sys
import urllib.request
import datetime
import time
import json
import requests

def get_request_url(url):
	req = urllib.request.Request(url)
	app_id = " sn0iHCAKHSIGvhB2qVvk"
	app_secret = "31psQcq5im"
	req.add_header("X-Naver-Client-ID", app_id)
	req.add_header("X-Naver-Client-Secret", app_secret)
	try:
		response=urllib.request.urlopen(req)
		if response.getcode() == 200:
			print("[%s]Url Request Success" %datetime.datetime.now())
			return response.read().decode("utf-8")
	except Exception as e:
		print(e)
		print("[%s] Error for URL : %s" %(datetime.datetime.now(), url))
		return None

def getURL(page_start) :
	client_id =  " sn0iHCAKHSIGvhB2qVvk"
	client_secret = "31psQcq5im"
	encText = urllib.parse.quote("서경대")
	url = "https://openapi.naver.com/v1/search/blog?query={}&start={}".format(encText,page_start)
	print(url)
	request = urllib.request.Request(url)
	request.add_header("X-Naver-Client-Id", client_id)
	request.add_header("X-Naver-Client-Secret", client_secret)

	response = urllib.request.urlopen(request)
	rescode = response.getcode()
	if (rescode == 200):
		response_body = response.read()
		return response_body.decode('utf-8')
	else:
		print("Error Code:" + rescode)

def getNaverSearchResult(sNode,search_text, page_start, display) :
	retData = getURL(page_start)
	print(retData)

	if retData is None :
		return None
	else:
		return json.loads(retData)

def getPostData(post, jsonResult):
	title = post['title']
	description = post['description']
	org_link = post["bloggerlink"]
	link = post['link']

	date = post["postdate"]

	postDate = datetime.datetime.strptime(date, '%Y%m%d')
	postDate = postDate.strftime('%Y-%m-%d %H: %M: %S')
	#print("Converted date string : {}".format(postDate))

	jsonResult.append({'title':title, 'description': description, 'org_link':org_link, 'link':org_link, 'postDate':postDate})

def main():
	sNode='blog'
	search_text = '서경대'
	cnt = 0
	jsonResult = []
	page_start=1

	while(True):
		jsonSearch = getNaverSearchResult(sNode, search_text, page_start, 100)
		page_start +=1
		total = jsonSearch['total']

		#print(total)

		for post in jsonSearch['items']:
			cnt = cnt + 1
			getPostData(post,jsonResult)
		if page_start > 100 :
			break

	print('전체 검색: %d 건' % total)
					   
	with open('./%s_naver_%s.json' %(search_text, sNode), 'w', encoding='utf-8' )as outfile:
		retJson = json.dumps(jsonResult, indent = 4, sort_keys=True, ensure_ascii=False)
		outfile.write(retJson)

	print("%s_naver_%s.json SAVED" %(search_text, sNode))
	print("가져온 데이터: %d 건" %(cnt))


if __name__ == "__main__" :
	main()
