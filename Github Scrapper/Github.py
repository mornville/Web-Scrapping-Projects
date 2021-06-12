import requests, re, json
from bs4 import BeautifulSoup

page = requests.get('https://www.codechef.com/users/mornville')
print(page)
page = page.text

soup = BeautifulSoup(page,"lxml")
#print(soup)
soup.prettify()
print(soup.title)
print(soup.title.text.split("-")[0])
try:
	avatar = soup.find_all("img", attrs={"class": "img-rounded","alt":"user avatar"})
	print("Avatar : ",avatar[0]['src'])
except:
	pass
name = soup.find_all("h4", attrs={"class": "realname"})
print("name : ",name[0].text.strip())
username = soup.find_all("p", attrs={"class": "username"})
print("username : ",username[0].text.strip())
try:
	desc = soup.find_all("i", attrs={"class": "fa-info"})
	print("desc : ",desc[0]['data-content'])
except:
	pass
js = soup.text
all_scripts = js.find('$("#github-connect").attr("href","') + len('$("#github-connect").attr("href","')
github_connect = ""
for i in js[all_scripts:]:
	if i == '"':
		break
	github_connect += i
print("Github : ",github_connect)
if '$("#google-connect").attr("href","' in js:
	all_scripts = js.find('$("#google-connect").attr("href","') + len('$("#google-connect").attr("href","')
	google_connect = ""
	for i in js[all_scripts:]:
		if i == '"':
			break
		google_connect += i
	print("Google : ",google_connect)
if '$("#facebook-connect").attr("href","' in js:
	all_scripts = js.find('$("#facebook-connect").attr("href","') + len('$("#facebook-connect").attr("href","')
	facebook_connect = ""
	for i in js[all_scripts:]:
		if i == '"':
			break
		facebook_connect += i
	print("Facebook : ",facebook_connect)

f1=open('leetcode.txt', 'wb+')
f1.write(soup.encode('utf-8'))