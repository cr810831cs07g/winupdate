# -*- coding: utf8 -*-
import requests, re
from bs4 import BeautifulSoup
import csv, pandas, time, random

headerlist = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36 OPR/43.0.2442.991",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36 OPR/42.0.2393.94",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36 OPR/47.0.2631.39",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
            "Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
            "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"]

user_agent = random.choice(headerlist)
headers = {'User-Agent': user_agent}
url = "https://www.catalog.update.microsoft.com/Search.aspx?q=10%20security"
result = requests.get(url, headers=headers)


soup = BeautifulSoup(result.text, 'html.parser')
title = []

t1 = soup.find_all("div"=="tableContainer" , class_ = 'contentTextItemSpacerNoBreakLink') # title
for link in t1:  
    title.append(link.text)

#goToDetails("49b17871-bef1-48b0-84cd-39e3b56f96ea");   36
str_pat = re.compile(r'\"(.*)\"')
regex = "([goToDetails])"
regex = "(r'\"(.*)\"')"
emails = re.find(regex, soup)
print()

regex = r'\bgoToDetails+(.*)'
t2 = re.findall(regex, str(t1))
#result = re.sub('\W+', '', value).replace("_", '')
t2 = [re.sub(r'("\r"|;|>|"\")', '', i) for i in t2]
t2 = [t2.sub('\r|"\"|;\>', '', i) for i in t2]
com1 = re.compile(r'\"(.*)\"')
t3 = com1.findall(str(t2))

