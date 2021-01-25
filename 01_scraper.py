import requests
from bs4 import BeautifulSoup
from time import sleep
from random import randint
from selenium import webdriver
import pandas as pd

# suppress geckodriver window
options = webdriver.FirefoxOptions()
options.add_argument('-headless')

# test geckodriver and selenium
drivertest = webdriver.Firefox(executable_path=r'C:\Users\leoba\PycharmProjects\JFscraper\geckodriver.exe')
drivertest.get("https://goabase.net")

# download website
page = requests.get("https://jf-archiv.de/archiv20.htm")
# check status
page.status_code
# check HTML text
if page.status_code == 200:
    print(page.text)
# parse site using bs4
soup = BeautifulSoup(page.content, 'html.parser')
print(soup.prettify())
list(soup.children)
[type(item) for item in list(soup.children)]
# find objects
soup.find_all('a')
# store urls
url = "https://jf-archiv.de/archiv20.htm"
headline = soup.find_all('a')
print(headline)
# isolate href attributes and store in dict
url_dict = {head.text: head['href'] for head in headline}
print(url_dict)
# store dict values in list and delete first entry
url_list = list(url_dict.values())
del url_list[0]
print(url_list)
len(url_list)
# append all list items to get complete urls
new_url_list = ['https://jf-archiv.de/' + s for s in url_list]
print(new_url_list)
len(new_url_list)
# scrape href attributes from all issues of that year
data = []
for i in range(0, 51):
    url1 = new_url_list[i]
    driver1 = webdriver.Firefox(executable_path=r'C:\Users\leoba\PycharmProjects\JFscraper\geckodriver.exe',options=options)
    driver1.get(url1)
    sleep(randint(1, 2))
    soup1 = BeautifulSoup(driver1.page_source, 'html.parser')
    article_urls_raw = soup1.find_all('a', {'href': True})

    for attribute in article_urls_raw:
        data.append(attribute)

    driver1.close()

print(data)
len(data)
# create dict with href values
article_urls_dict = {attribute.text: attribute['href'] for attribute in data}
len(article_urls_dict)
print(article_urls_dict)
# create list with values
article_urls_list = list(article_urls_dict.values())
print(article_urls_list)
# extract htm strings only
subs = 'htm'
a_url_new = [i for i in article_urls_list if subs in i]
print(a_url_new)
len(a_url_new)
# append all list items to get complete urls
really_new_aurl = ['https://jf-archiv.de/archiv20/' + x for x in a_url_new]
print(really_new_aurl)
len(really_new_aurl)
# retrieve text data
date = []
title = []
url = []
text = []
for i in range(0, 3010):
    url2 = really_new_aurl[i]

    response = requests.get(url2)
    if response.status_code != 200:
        continue

    driver2 = webdriver.Firefox(executable_path=r'C:\Users\leoba\PycharmProjects\JFscraper\geckodriver.exe',options=options)
    driver2.get(url2)
    sleep(randint(1, 2))
    soup2 = BeautifulSoup(driver2.page_source, 'html.parser')

    adate = soup2.find('title')
    bdate = adate.get_text()
    cdate = bdate.split('/')[0].strip()
    date.append(cdate)

    atitle = soup2.find('title')
    btitle = atitle.get_text()
    ctitle = btitle.split('/')[-1].strip()
    title.append(ctitle)

    url.append(url2)

    atext = soup2.find_all('p')
    btext = [tag.get_text().strip() for tag in atext]
    text.append(btext)

    driver2.close()

# create dataframe
yeardf = pd.DataFrame({
    "date": date,
    "title": title,
    "url": url,
    "text": text
})

# add missing year values to date strings (until 2003; 2010; 2017)
date_list = yeardf['date'].tolist()
new_date = [s + '17' for s in date_list]
new_date[:] = [elem[:8] for elem in new_date]
yeardf['new_date'] = new_date
yeardf = yeardf.drop(['date'], axis=1)
yeardf = yeardf[['new_date','title','url','text']]
yeardf = yeardf.rename(columns={'new_date': 'date'})

# add missing date values (volumes 2004-2006)
yeardf['date'] = yeardf['date'].replace(['22.'],'22.12.06')
yeardf['date'] = yeardf['date'].replace(['28.07.'],'28.07.06')

# export to csv
yeardf.to_csv('jf_20_raw.csv')
