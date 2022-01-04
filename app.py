from logger_class import getLog
from flask import Flask, render_template, request, jsonify, Response, url_for, redirect
from flask_cors import CORS, cross_origin
from mongoDBOperations import MongoDBManagement
from WikiScrapping import WikiScrapper
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

logger = getLog('wiki.py')
db_name ='Wiki-Scrapper'
searchString = None


app = Flask(__name__) ## Initialising the flask app with the name 'app'

## for selenium driver implementation on heroku
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("disable-dev-shm-usage")

@app.route('/',methods=['POST','GET'])
@cross_origin()
def index():
    if request.method =='POST':
        global searchString
        searchString = request.form['content']  #obtaining the search string entered in the form
        try:
            scrapper_object = WikiScrapper(executable_path = ChromeDriverManager().install(),
                                           chrome_options=chrome_options)
            mongoClient = MongoDBManagement(username='vijaya',password='atlas')
            scrapper_object.openUrl("https://www.wikipedia.org/")
            logger.info("Url hitted")
            scrapper_object.searchdata(searchString=searchString)
            logger.info(f"Search begins for {searchString}")
            searchString = scrapper_object.get_heading()
            if mongoClient.isCollectionPresent(collection_name=searchString,db_name=db_name):
                response = mongoClient.findAllRecords(db_name=db_name,collection_name=searchString)
                response_list = [i for i in response]
                result = scrapper_object.get_Summ_FromDB(result=response_list)
                heading = scrapper_object.get_Heading_FromDB(result=response_list)
                scrapper_object.saveDataTotxt(data=result,file_name="static/scrapper_data.txt")
                logger.info("Summarized Data saved in scrapper file")
                return render_template('results.html',result=result,obj = heading) ## show the results to user
            else:
                records_toDB = scrapper_object.insertRecordsIntoDb(searchString) ## To store summarization,reference links and base64 images into database
                logger.info("Summarized data, references links and images stored in db ")
                print(records_toDB)
                heading = scrapper_object.get_heading()
                text = scrapper_object.getSummText(searchString)
                logger.info("Text summarized")
                return render_template('results.html', result=text, obj = heading)
        except Exception as e:
            raise Exception(f"(app.py) - Something went wrong while rendering the search \n" + str(e))
    else:
        return render_template('index.html')


@app.route('/references',methods=['GET'])
def references():
    try:
        global searchString
        if searchString is not None:
            scrapper_object = WikiScrapper(executable_path=ChromeDriverManager().install(),
                                           chrome_options=chrome_options)
            mongoClient = MongoDBManagement(username='vijaya', password='atlas')
            if mongoClient.isCollectionPresent(collection_name=searchString, db_name=db_name):
                response = mongoClient.findAllRecords(db_name=db_name, collection_name=searchString)
                response_list = [i for i in response]
                result = scrapper_object.get_links_FromDB(result=response_list)
                heading = scrapper_object.get_Heading_FromDB(result=response_list)
                scrapper_object.saveDataTotxt(data=result, file_name="static/scrapper_links.txt")
                logger.info("Reference links saved in scrapper file")
                if len(result) == 0:
                    no_references = "No references found in wikipedia"
                    return render_template('notfound.html', result=no_references, obj=heading)
                else:
                    return render_template('references.html', result=result,obj = heading)
            else:
                heading = scrapper_object.get_heading()
                ref_links = scrapper_object.getLinks(searchString)
                logger.info("Reference links obtained")
                return render_template('references.html', result=ref_links,obj = heading)
        else:
            return render_template('references.html', result=None)
    except Exception as e:
        raise Exception("f(references): Something went wrong while rendering the references links \n")


@app.route('/images',methods=['GET'])
def images():
    try:
        global searchString
        if searchString is not None:
            scrapper_object = WikiScrapper(executable_path=ChromeDriverManager().install(),
                                              chrome_options=chrome_options)
            mongoClient = MongoDBManagement(username='vijaya', password='atlas')
            if mongoClient.isCollectionPresent(collection_name=searchString, db_name=db_name):
                response = mongoClient.findAllRecords(db_name=db_name, collection_name=searchString)
                response_list = [i for i in response]
                heading = scrapper_object.get_Heading_FromDB(result=response_list)
                result = scrapper_object.get_images_FromDB(result=response_list)
                scrapper_object.saveDataTotxt(data=result, file_name="static/scrapper_images.txt")
                logger.info("Image links saved in scrapper file")
                if len(result) == 0:
                    no_images = "No images found in wikipedia"
                    return render_template('notfound.html',result=no_images,obj = heading)
                else:
                    return render_template('images.html', result=result,obj=heading)
            else:
                heading = scrapper_object.get_heading()
                images = scrapper_object.getImages(searchString)
                logger.info("Images obtained")
                if len(images) == 0:
                    return render_template('notfound.html',obj = heading)
                else:
                    return render_template('images.html', result=images,obj = heading)

        else:
            return render_template('images.html', result=None)
    except Exception as e:
        raise Exception("f(images): Something went wrong while rendering the images \n")


if __name__ == "__main__":
    app.run(port=2000,debug=True) # running the app on the local machine on port 5000



## https://wikiscrapper.herokuapp.com/