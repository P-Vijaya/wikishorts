import pymongo
import pandas as pd
import json


class MongoDBManagement:
    def __init__(self,username,password):
        """
        This function sets the required url
        """
        try:
            self.username = username
            self.password = password
            self.url = "mongodb+srv://vijaya:atlas@cluster0.6nhgw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority".format(
                self.username, self.password)
        except Exception as e:
            raise Exception(f"(__init__): Something went wrong on initiation process\n"+str(e))

    def getMongoDBClientObject(self):
        """
        This function creates the client object for connection purpose
        """
        try:
            mongo_client =pymongo.MongoClient(self.url)
            return mongo_client
        except Exception as e:
            raise Exception("(getMongoDBClientObject): Someting went wrong on creation of client objec\n"+str(e))

    def closeMongoDBConnection(self,mongo_client):
        """
        This function closes the connectionof client
        """
        try:
            mongo_client.close()
        except Exception as e:
            raise Exception(f"Something went wrong on closing connection\n"+str(e))

    def isDatabasePresent(self,db_name):
        """
        This function checks if the database is present or  not
        """
        try:
            mongo_client = self.getMongoDBClientObject()
            if db_name in mongo_client.list_database_names():
                mongo_client.close()
                return True
            else:
                mongo_client.close()
                return False
        except Exception as e:
            raise Exception("(isDatabasePresent): Failed in checking if the database is present or not \n"+ str(e))


    def createDatabase(self,db_name):
        """
        This function creates database
        """
        try:
            database_check_status = self.isDatabasePresent(db_name=db_name)
            if not database_check_status:
                mongo_client = self.getMongoDBClientObject()
                database = mongo_client[db_name]
                mongo_client.close()
                return database
            else:
                mongo_client = self.getMongoDBClientObject()
                database = mongo_client[db_name]
                mongo_client.close()
                return database
        except Exception as e:
            raise Exception(f"(createDatabase): Failed on creating database\n"+str(e))

    def dropDatabase(self,db_name):
        """
        This function deletes the database from MongoDB
        """
        try:
            mongo_client = self.getMongoDBClientObject()
            if db_name in mongo_client.list_database_names():
                mongo_client.drop_database(db_name)
                mongo_client.close()
                return True
        except Exception as e:
            raise Exception(f"(dropDatabase): Failed to delete database {db_name}\n"+str(e))

    def getDatabase(self,db_name):
        """
        This function return database
        """
        try:
            mongo_client = self.getMongoDBClientObject()
            mongo_client.close
            return mongo_client[db_name]
        except Exception as e:
            raise Exception(f"(getDatabase): Failed to get the database list")

    def getCollection(self,collection_name,db_name):
        """
        This function return collection
        """
        try:
            database = self.getDatabase(db_name)
            return database[collection_name]
        except Exception as e:
            raise Exception(f"(getCollection): Failed to get the database list")

    def isCollectionPresent(self,collection_name,db_name):
        """
        This checks if collection is present or not
        """
        try:
            database_status = self.isDatabasePresent(db_name = db_name)
            if database_status:
                database = self.getDatabase(db_name=db_name)
                if collection_name in database.list_collection_names():
                    return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            raise Exception(f"(isCollectionPresent): Failed to check collection\n"+str(e))

    def createCollection(self,collection_name, db_name):
        """
        This function creates collection in the database given
        """
        try:
            collection_check_status = self.isCollectionPresent(collection_name=collection_name,db_name=db_name)
            if not collection_check_status:
                database = self.getDatabase(db_name=db_name)
                collection = database[collection_name]
                return collection
        except Exception as e:
            raise Exception(f"(createCollection): Failed to create collection {collection_name}\n"+str(e))

    def dropCollection(self,collection_name,db_name):
        """
        This function drops the collection
        """
        try:
            collection_check_status =self.isCollectionPresent(collection_name=db_name,db_name=db_name)
            if collection_check_status:
                collection = self.getCollection(collection_name=collection_name,db_name=db_name)
                collection.drop()
                return True
            else:
                return False
        except Exception as e:
            raise Exception(f"(dropCollection): Failed to drop collection {collection_name}\n"+str(e))

    def insertRecord(self,db_name,collection_name,record):
        """
        This function inserts a record
        """
        try:
            collection = self.getCollection(collection_name=collection_name,db_name=db_name)
            collection.insert_one(record)
            sum = 0
            return f"rows inserted"
        except Exception as e:
            raise Exception(f"(insertRecord): Something went wrong on inserting a record\n"+str(e))

    def insertRecords(self,db_name,collection_name,records):
        """
        This functions inserts records
        """
        try:
            collection = self.getCollection(collection_name=collection_name,db_name=db_name)
            record = list(records.values())
            collection.insert_many(record)
            sum = 0
            return f"rows inserted"
        except Exception as e:
            raise Exception(f"(insertRecords): Something went wrong on inserting records\n"+str(e))


    def findfirstRecord(self,db_name,collection_name,query=None):
        """
        This function finds record for the given collection and database
        """
        try:
            collection_check_status = self.isCollectionPresent(collection_name=collection_name,db_name=db_name)
            if collection_check_status:
                collection = self.getCollection(collection_name=collection_name,db_name=db_name)
                firstRecord =collection.find_one(query)
                return firstRecord
        except Exception as e:
            raise Exception(f"(findfirstRecord): Failed to find record of the given collection and database\n" + str(e))


    def findAllRecords(self,db_name,collection_name):
        """
        This function finds records for the given collection and database
        """
        try:
            collection_check_status = self.isCollectionPresent(collection_name=collection_name,db_name=db_name)
            if collection_check_status:
                collection =self.getCollection(collection_name=collection_name,db_name=db_name)
                findAllRecords =collection.find()
                return findAllRecords
        except Exception as e:
            raise Exception(f"(findAllRecords): Failed to find records for the given collection and database\n" + str(e))


    def findRecordOnQuery(self,db_name,collection_name,query):
        """
        This function finds record for the given query,collection or database
        """
        try:
            collection_check_status =self.isCollectionPresent(collection_name=collection_name,db_name=db_name)
            if collection_check_status:
                collection = self.getCollection(collection_name=collection_name,db_name=db_name)
                findRecords = collection.find(query)
                return findRecords
        except Exception as e:
            raise Exception(f"(findRecordOnQuery): Failed to find record for the given query,collection or database\n" + str(e))

    def updateOneRecord(self,db_name,collection_name,query):
        """
        This function to update a record with given collection query or database name
        """
        try:
            collection_check_status = self.isCollectionPresent(collection_name=collection_name,db_name=db_name)
            if collection_check_status:
                collection = self.getCollection(collection_name=collection_name,db_name=db_name)
                previous_records = self.findAllRecords(db_name=db_name,collection_name=collection_name)
                new_records = query
                updated_record =collection.update_one(previous_records,new_records)
                return updated_record
        except Exception as e:
            raise Exception(f"(updateOneRecord): Failed to update a record with given collection query or database name\n" + str(e))


    def updateMultipleRecord(self,db_name,collection_name,query):
        """
        This function to update the records with given collection name, query or database name
        """
        try:
            collection_check_status = self.isCollectionPresent(collection_name=collection_name,db_name=db_name)
            if collection_check_status:
                collection = self.getCollection(collection_name=collection_name,db_name=db_name)
                previous_records = self.findAllRecords(db_name=db_name,collection_name=collection_name)
                new_records = query
                updated_record = collection.update_many(previous_records,new_records)
                return updated_record
        except Exception as e:
            raise Exception(f"(updateMultipleRecord): Failed to update the records with given collection name, query or database name\n" + str(e))

    def deleteRecord(self,db_name,collection_name,query):
        """
        This function to delete the record with given collection query or database name
        """
        try:
            collection_check_status = self.isCollectionPresent(collection_name=collection_name,db_name=db_name)
            if collection_check_status:
                collection = self.getCollection(collection_name=collection_name,db_name=db_name)
                collection.delete_one(query)
                return "1 row deleted"
        except Exception as e:
            raise Exception(f"(deleteRecord): Failed to delete the record with given collection query or database name\n" + str(e))

    def deleteRecords(self,db_name,collection_name,query):
        """
        This function to delete the records with given collection query or database name
        """
        try:
            collection_check_status = self.isCollectionPresent(collection_name=collection_name,db_name=db_name)
            if collection_check_status:
                collection = self.getCollection(collection_name=collection_name,db_name=db_name)
                collection.delete_many(query)
                return "Multiple rows deleted"
        except Exception as e:
            raise Exception(f"(deleteRecords): Failed to delete the records with given collection query or database name\n" + str(e))

    def getDataFrameofCollection(self,db_name,collection_name):
        """
        THis function to get DatFrame from provided collection and database
        """
        try:
            all_Records =self.findAllRecords(db_name=db_name,collection_name=collection_name)
            dataframe =pd.DataFrame(all_Records)
            return dataframe
        except Exception as e:
            raise Exception(f"(getDataFrameofCollection):Failed to get DatFrame from provided collection and database\n" + str(e))

    def saveDataFrameIntoCollection(self,collection_name,db_name,dataframe):
        """
        This function to save dataframe value into collection
        """
        try:
            collection_check_status = self.isCollectionPresent(collection_name=collection_name,db_name=db_name)
            dataframe_dict = json.loads(dataframe.T.to_json())
            if collection_check_status:
                self.insertRecords(db_name=db_name,collection_name=collection_name,records=dataframe_dict)
                return "Inserted"
            else:
                self.createDatabase(db_name=db_name)
                self.createCollection(collection_name=collection_name,db_name=db_name)
                self.insertRecords(db_name=db_name,collection_name=collection_name,records=dataframe_dict)
                return "Inserted"
        except Exception as e:
            raise Exception(f"(saveDataFrameIntoCollection):Failed to save dataframe value into collection\n" + str(e))

    def getResultsToDisplayOnBrowser(self,db_name,collection_name):
        """
        This function returns the final result to display on browser.
        """
        try:
            response =self.findAllRecords(db_name=db_name,collection_name=collection_name)
            result =[i for i in response]
            return result
        except Exception as e:
            raise Exception(f"(getResultsToDisplayOnBrowser): Something went wrong on getting result from database\n" + str(e))
