##for an ethical scraping first check the website as in which data are you allowed  scrap by : "<website-name>/robots.txt"

# setting environment for scraping...
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import unittest, time, re, random
import urllib
from bs4 import BeautifulSoup
# import xlwt
# from xlwt import Workbook
import csv

# initializaing variables...
scrapedData = None
# wb = Workbook()

url = 'http://books.toscrape.com/index.html'

# using chrome driver
#executable_path='C:/Users/COMPAQ/chromedriver'
driver = webdriver.Chrome(executable_path='C:/Users/Khushbu Nakum/PycharmProjects/scraper/chromedriver')
driver.maximize_window()
driver.implicitly_wait(10)


class Scraping:

    def parseUrl(self, url):
        #print("Parsing url :" + url)

        try:

            driver.get(url)
            #time.sleep(random.randrange(5, 10))
            page = driver.page_source

            soup = BeautifulSoup(page, "html.parser")

            return soup

        except Exception as e:
            print("Error: " + str(e))

    def getProductUrl(self, url):

        try:
            soup = self.parseUrl(url)
            # links = soup.find('article',class_='product_pod').div.a.get('href')
            # print(links)

            mainPageProductUrl = ["/".join(url.split("/")[:-1]) + "/" + x.div.a.get('href') for x in
                                  soup.find_all('article', class_='product_pod')]
            # print(str(len(mainPageProductUrl)) + " fetched products Url")
            # print("Product Example :")
            # print(mainPageProductUrl[0])

            return mainPageProductUrl

        except Exception as e:
            print("Error: " + str(e))

    def getBookUrl(self, url):

        #print("Fetching Books Url :" + url)

        try:
            pageUrl = [url]
            # print(pageUrl[0])
            soup = self.parseUrl(pageUrl[0])

            while len(soup.find_all('a', href=re.compile(r'page.*'))) == 2 or len(pageUrl) == 1:
                newUrl = "/".join(pageUrl[-1].split("/")[:-1]) + "/" + soup.find_all('a', href=re.compile(r'page.*'))[
                    -1].get('href')
                pageUrl.append(newUrl)

                soup = self.parseUrl(newUrl)

            # pageUrl =soup.find_all('a', href = re.compile(r'page.*'))

            # print(str(len(pageUrl)) + " fetched urls")
            # print("Page Url : ")
            # print(pageUrl[:2])

            booksUrl = []
            #print("Fetching product Url from {} Pages :" %len(pageUrl))
            for page in pageUrl:
                productUrl = self.getProductUrl(page)
                booksUrl.extend(productUrl)

            # print(str(len(booksUrl)) + "fetched Urls")
            # print("Books Url " + booksUrl[:3])

            return booksUrl



        except Exception as e:
            print("Error :" + str(e))

    def scrapData(self, url):

        name = []
        imgUrl = []
        category = []

        print("Scraping Url : " + url)
        try:
            # print("Calling Book function..")
            baseUrl = url
            booksUrl = self.getBookUrl(baseUrl)
            #print("Saving {} data..." %len(booksUrl))
            for url in booksUrl:
                soup = self.parseUrl(url)
                name.append(soup.find('div', class_=re.compile("product_main")).h1.text)
                imgUrl.append(url.replace("index.html", "") + soup.find("img").get("src"))
                #category.append(soup.find("a", href=re.compile("../category/books/")).get("href").split("/")[3])

                scrapData = str(name) + ', ' + str(imgUrl)

            with open('books_details.csv', 'a') as file:
                file.write(scrapData)

            print("Data saved!")

        except Exception as e:
            print("Error :" + str(e))

            # If we want to scrap a specific part of a website
            '''
            categoriesUrl = [url + x.get('href') for x in soup.find_all('a', href= re.compile(r'catalogue/category/books/.*'))] 
            categoriesUrl = categoriesUrl[1:] #first link corresponds to all the books

            print(str(len(categoriesUrl)) + " fetched categories Url")
            print("Category Example :" + categoriesUrl[:3])
            '''


if __name__ == "__main__":
    scrap = Scraping()
    scrap.scrapData(url)

# scrap.scrapData(url)





