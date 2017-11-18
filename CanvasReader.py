import time
# need to install if not installed:
# pip install splinter
import getpass

from splinter import Browser
# need to install if not installed:
# pip install wordcloud
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# demonstrate how to automatically pull posts from Canvas discussion board and create a word cloud

# the path of your downloaded chromedrive from https://sites.google.com/a/chromium.org/chromedriver/downloads
chromedriverPath = '/uufs/chpc.utah.edu/common/home/u0876964/local/software/browser_drivers/chromedriver'

# url of the discussion board
url = 'https://utah.instructure.com/courses/459611/discussion_topics/2070560'

# your user name
username = ''
# your canvas password
# password = ''
password = getpass.getpass('password:')

# which duo authentication device is going to be used
duo_device_num = 0

f = open("discusion.txt", "w", encoding="utf-8")

browser = Browser('chrome', executable_path=chromedriverPath)
# browser = Browser('chrome', headless=False, executable_path=chromedriverPath)
# browser = Browser('firefox',executable_path=geckoPath)
# url = "http://www.google.com"
browser.visit(url)

browser.fill('username', username)
browser.fill('password', password)
browser.find_by_name('submit').click()

with browser.get_iframe('duo_iframe') as iframe:
	device = iframe.find_by_tag('select').first
	options = iframe.find_by_tag('option')
	device.select(options[duo_device_num].value)
	buts = iframe.find_by_tag('button')
	for but in buts:
		if but.visible:
			but.click()
			break

eles = browser.find_by_css(".message.user_content.enhanced")
while eles is None or len(eles) < 3:
	time.sleep(1)
	eles = browser.find_by_css(".message.user_content.enhanced")
	print("waiting duo authentication...")
posts = []
print("page loaded.")
time.sleep(5)
for content in eles:
	f.write(content.value)
	posts.append(content.value)
	print(content.value)
f.close()

text = '\n'.join(posts)
print(text)

wordcloud = WordCloud().generate(text)

wordcloud = WordCloud(max_font_size=40).generate(text)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
