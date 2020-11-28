import urllib.request
from urllib.parse import urlparse
import uuid

import re
import os
import requests
from bs4 import BeautifulSoup
import archiever

max_urls = 50
site = "http://www.exemple.com"


class UrlScraper:
    def __init__(self, site, amountOfLinks=-1):
        self.site = site
        self.domain = urlparse(site).netloc
        self.amountOfLinks = amountOfLinks
        self.urllist = []
        self.scrape(self.site)

    def scrape(self, link):
        try:
            links = re.findall(
                r"""<\s*a\s*href=["']([^=]+)["']""", urllib.request.urlopen(link).read().decode("utf-8"))
            for item in links:
                print(item)
                if self.domain not in item:
                    if(str(item).startswith("/")):
                        pass
                    else:
                        continue
                if 'http' not in item:
                    item = '{}{}'.format(self.site, item)
                self.urllist.append(item)
        except Exception as ex:
            print(ex)


class ImgScraper:
    def __init__(self):
        pass

    def scrape(self, site):
        response = requests.get(site)

        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags = soup.find_all('img')
        urls = []
        try:
            for item in img_tags:
                urls.append(item.get('src'))
            #urls = [img['src'] for img in img_tags]
        except Exception as ex:
            print(ex)

        print(len(urls))

        domain = urlparse(site).netloc
        print(domain)
        if not os.path.exists(domain):
            os.makedirs(domain)
        for url in urls:
            filename = re.search(r'/([\w_-]+[.](jpg|gif|jpeg|png))$', str(url))
            if not filename:
                #print("Regex didn't match with the url: {}".format(url))
                continue
            if(url not in visitedUrls):
                archiever.archieveUrl(url)
                with open(domain+"/"+str(uuid.uuid4())+filename.group(1), 'wb') as f:
                    #print("filename ::  "+domain+"/" +str(uuid.uuid4())+filename.group(1))
                    #print(filename.group(1))
                    if 'http' not in url:
                        # sometimes an image source can be relative
                        # if it is provide the base url which also happens
                        # to be the site variable atm.
                        url = '{}{}'.format(site, url)
                    response = requests.get(url)
                    f.write(response.content)
            else:
                print("image {} already exist in history ".format(filename.group(1)))


scraper = UrlScraper(site, max_urls)
imgScraper = ImgScraper()

visitedUrls = archiever.loadVisitedUrls()



for ll in scraper.urllist:
    imgScraper.scrape(ll)
