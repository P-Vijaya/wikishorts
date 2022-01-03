import base64
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from RepositoryForObject import ObjectRepository
from selenium.webdriver.common.by import By


from mongoDBOperations import MongoDBManagement
import nltk
nltk.download(['stopwords', 'punkt'])
from summarize import summarize
import re
import requests
from bs4 import BeautifulSoup


class WikiScrapper:
    def __init__(self,executable_path,chrome_options):
        """
        This function initializes the web browser driver
        """
        try:
            self.driver = webdriver.Chrome(executable_path=executable_path,chrome_options=chrome_options)
        except Exception as e:
            raise Exception(f"(__init__): Something went wrong on initializing the web driver object\n"+str(e))

    def waitExplicitlyForCondition(self, element_to_be_found):
        """
        This function explicitly for condition to satisfy
        """
        try:
            ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)
            WebDriverWait(self.driver, 2, ignored_exceptions=ignored_exceptions).until(
                expected_conditions.presence_of_element_located((By.CLASS_NAME, element_to_be_found)))
            return True
        except Exception as e:
            return False

    def openUrl(self,url):
        """
        This function opens the particular url passed
        """
        try:
            if self.driver:
                self.driver.get(url)
                return True
            else:
                return False
        except Exception as e:
            raise Exception(f"(openUrl) - Something went wrong on opening the url {url}.\n" + str(e))

    def getLocatorsObject(self):
        """
        This function initializes the locator object and returns the locator object
        """
        try:
            locators = ObjectRepository()
            return locators
        except Exception as e:
            raise Exception(f"(getLocatorObject) - Could not find locators\n" + str(e))

    def findElementByXpath(self,xpath):
        """
        This function finds the web element using xpath passed
        """
        try:
            element = self.driver.find_element(By.XPATH,value=xpath)
            return element
        except Exception as e:
            raise Exception(f"(findElementByXpath) - XPATH provided was not found. \n" + str(e))

    def searchdata(self,searchString):
        """
        This function help to search information using search string provided by the user
        """
        try:
            locator = self.getLocatorsObject()
            search_box_path = self.findElementByXpath(xpath=locator.getInputSearchArea()).send_keys(searchString)
            self.waitExplicitlyForCondition(search_box_path)
            first_suggestion = self.findElementByXpath(xpath=locator.getfirstsuggestion())
            text = first_suggestion.get_attribute("innerText")
            if "Topics" in text:
                second_suggestion = self.findElementByXpath(xpath=locator.getsecondsuggestion())
                second_suggestion.click()
            else:
                first_suggestion.click()
            return True
        except Exception as e:
            raise Exception(f"(searchProduct) - Something went wrong on searching.\n" + str(e))

    def saveDataFrameToFile(self,dataframe,file_name):
        """
        This function saves dataframe into filename given
        """
        try:
            dataframe.to_csv(file_name)
        except Exception as e:
            raise Exception(f"(saveDataFrameToFile) - Unable to save data to the file.\n" + str(e))

    def saveDataTotxt(self,data,file_name):
        """
        This function saves data to a text file
        """
        try:
            text_file = open(file_name,"w")
            text_file.write(str(data))
            text_file.close()
        except Exception as e:
            raise Exception(f"(saveSummDataTocsv) - Unable to save data to the text file.\n" + str(e))


    def getTextfromWiki(self,searchString):
        """
        This function will get text from the wiki page
        """
        try:
            wikiSelect = "https://en.wikipedia.org/wiki/{}".format(searchString)
            html = requests.get(wikiSelect)
            wiki_html = BeautifulSoup(html.text,"html.parser")
            paragraphs = wiki_html.findAll('p')
            #paragraphs = BeautifulSoup(str(para),"html.parser")
            wiki_text = ""
            for p in paragraphs:
                wiki_text += p.text
            return wiki_text
        except Exception as e:
            raise Exception(f"(getSummParasToDisplay) - Something went wrong while getting text from wiki.\n" + str(e))


    def getSummText(self,searchString):
        """
        The function will summarize the text obtained from wiki
        """
        try:
            scrapper_wiki = self.getTextfromWiki(searchString=searchString)
            document = re.sub(r'[[0-9]*]',' ',scrapper_wiki)
            document.replace('{','')
            document.replace('}','')
            document = re.sub(r'[,]', '', document)
            summ = summarize(document, sentence_count=18, language='english')
            return summ
        except Exception as e:
            raise Exception(f"(summText) - Something went wrong while summarizing the text.\n" + str(e))



    def getLinks(self,searchString):
        """
        This function will help to fetch links from references in wiki's page
        :return:
        """
        try:
            modules = []
            session = requests.Session()
            wikiSelect = "https://en.wikipedia.org/wiki/{}".format(searchString)
            html = session.post(wikiSelect)
            wiki_html = BeautifulSoup(html.text, "html.parser")
            href_url = wiki_html.findAll('span', {'class': 'reference-text'})
            href = BeautifulSoup(str(href_url), "html.parser")
            link_href = [a["href"] for a in href.find_all("a", href=True)]
            for link in link_href:
                if link[1] == 'w':
                    full_link = "https://en.wikipedia.org" + link
                    modules.append(full_link)
                elif link[1] == 'c':
                    continue
                else:
                    modules.append(link)
            return modules

        except Exception as e:
            raise Exception(f"(getLinks): - something went wrong while fetching links")

    def getImages(self,searchString):
        """
        This function will get all the images from the selected wiki page
        """
        try:
            wikiSelect = "https://en.wikipedia.org/wiki/{}".format(searchString)
            html = requests.get(wikiSelect)
            wiki_html = BeautifulSoup(html.content)
            images_url = wiki_html.findAll('img', {'src': re.compile('.jpg')})
            images = [image_url['src'] for image_url in images_url]
            return images
        except Exception as e:
            raise Exception(f"(getImages): - something went wrong while fetching images")

    def get_heading(self):
        """
        This function will get the heading of the wikipedia page
        """
        try:
            element = self.driver.find_element(By.ID,'firstHeading')
            name = element.get_attribute("innerText")
            return name
        except Exception as e:
            raise Exception(f"(get_heading) - Something went wrong while scrapping the heading.\n" + str(e))


    def imageurl_to_base64(self,url):
        """
        This function will convert the image's url to base 64
        """
        try:
            return base64.b64encode(requests.get(url).content)
        except Exception as e:
            raise Exception(f"(url_to_base64): - something went wrong while converting image's url to base64")


    def insertRecordsIntoDb(self,searchString):
        """
        #This function is for inserting records such as summarization data,ref_links and images
        :return:
        """
        try:
            images_base64 = []
            mongoClient = MongoDBManagement(username='vijaya', password='atlas')
            heading = self.get_heading()
            summ = self.getSummText(searchString=searchString)
            links = self.getLinks(searchString=searchString)
            images = self.getImages(searchString=searchString)
            for i in images:
                full_link = "https:" + i
                base64_url = self.imageurl_to_base64(full_link)
                images_base64.append(base64_url)
            result = {'wiki_heading':heading,
                      'summ_data': summ,
                      'ref_links': links,
                      'wiki_images': images,
                      'images_64':images_base64}
            mongoClient.insertRecord(db_name="Wiki-Scrapper", collection_name=searchString, record=result)
            return "Sucessfully inserted into db"
        except Exception as e:
            raise Exception(f"(insertRecordsIntoDb): - something went wrong while inserting records such as summarization data ,ref_links and images")


    def get_Heading_FromDB(self,result):
        """
        This function will fetch heading from db
        """
        try:
            for i in result:
                if type(i) == dict:
                    data_heading = i.get("wiki_heading")
            return data_heading
        except Exception as e:
            raise Exception(
                f"(get_Heading_FromDB) - Something went wrong while fetching heading from db.\n" + str(e))


    def get_Summ_FromDB(self,result):
        """
        This function will fetch summarization data from db
        """
        try:
            for i in result:
                if type(i) == dict:
                    data_summ = i.get("summ_data")
            return data_summ
        except Exception as e:
            raise Exception(f"(get_Summ_FromDB) - Something went wrong while fetching summarization data from db.\n" + str(e))


    def get_links_FromDB(self,result):
        """
        This function will fetch reference links from db
        """
        try:
            for i in result:
                if type(i) == dict:
                    links = i.get("ref_links")
            return links
        except Exception as e:
            raise Exception(f"(get_links_FromDB) - Something went wrong while fetching reference links from db.\n" + str(e))


    def get_images_FromDB(self,result):
        """
        This function will fetch images from db
        """
        try:
            for i in result:
                if type(i) == dict:
                    images = i.get("wiki_images")
            return images
        except Exception as e:
            raise Exception(f"(get_links_FromDB) - Something went wrong while fetching reference links from db.\n" + str(e))

    def get_heading(self):
        """
        This function will get the heading of the wikipedia page
        """
        try:
            element = self.driver.find_element(By.ID,'firstHeading')
            name = element.get_attribute("innerText")
            return name
        except Exception as e:
            raise Exception(f"(get_heading) - Something went wrong while scrapping the heading.\n" + str(e))


