# -*- coding: utf8 -*-
import requests, re
from bs4 import BeautifulSoup
import csv, pandas, time, random

site = input("Microsoft Update Catalog Search: ")

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36'}
url = "https://www.catalog.update.microsoft.com/Search.aspx?q=" + site
result = requests.get(url, headers=headers)

with open( site + '.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['Title', 'Catalog Link', 'Download Link'])

    soup = BeautifulSoup(result.text, 'html.parser')
    title = []
    t1 = soup.find_all("div"=="tableContainer" , class_ = 'contentTextItemSpacerNoBreakLink')
    for link in t1:  
        title.append(link.text)     # title

    c_url = 'https://www.catalog.update.microsoft.com/ScopedViewInline.aspx?updateid='   
    urllist = []
    catalog_url = []
    regex = r'\bgoToDetails+(.*)'
    tmp_reg = r'\".*\"'
    t2 = re.findall(regex, str(t1))
    for i in t2:
        tmp_reg = re.compile(r'\w.*\w')
        tmp_match = tmp_reg.search(i)
        #print(tmp_match.group(0))
        catalog_url.append(c_url + tmp_match.group(0))    # catalog url
        urllist.append(tmp_match.group(0))

    i_count = 0
    url_t = "https://www.catalog.update.microsoft.com/DownloadDialog.aspx"
    download_link = []
    for i in urllist:
        payload_t = "updateIDs=[{\"size\":0,\"languages\":\"\",\"uidInfo\":\"%s\",\"updateID\":\"%s\"}]"%(i,i)
        headers_t = {
        'Cache-Control': 'max-age=0',
        'Sec-Ch-Ua': '"(Not(A:Brand";v="8", "Chromium";v="101"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'https://www.catalog.update.microsoft.com',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://www.catalog.update.microsoft.com/DownloadDialog.aspx',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7'
        }
        response = requests.request("POST", url_t, headers=headers_t, data=payload_t)
        res_reg = re.compile(r'https.*cab')
        res_match = res_reg.search(response.text)
        download_link.append(res_match.group(0))        # download link
        writer.writerow([title[i_count+1], catalog_url[i_count], download_link[i_count]])
        i_count = i_count + 1
        print(res_match.group(0))
