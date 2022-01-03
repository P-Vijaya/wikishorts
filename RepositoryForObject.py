class ObjectRepository:

    def __init__(self):
        print()

    def getInputSearchArea(self):
        search_inputarea = "/html[1]/body[1]/div[3]/form[1]/fieldset[1]/div[1]/input[1]"
        return search_inputarea

    def getSearchButton(self):
        search_button = "/html[1]/body[1]/div[3]/form[1]/fieldset[1]/button[1]"
        return search_button

    def getfirstsuggestion(self):
        first_suggestion  = "/html/body/div[3]/form/fieldset/div/div[2]/div/a[1]"
        return first_suggestion

    def getsecondsuggestion(self):
        second_suggestion  = "/html/body/div[3]/form/fieldset/div/div[2]/div/a[2]"
        return second_suggestion

    def getTextfromweb(self):
        text = "/html/body/div[3]/div[3]/div[5]/div[1]"
        return text

    def getReferenceHeader(self):
        ref_header = "/html/body/div[3]/div[3]/div[5]/div[1]/h2[13]/span[1]"
        return ref_header

    def getReferenceLink(self):
        ref = "/html/body/div[3]/div[3]/div[5]/div[1]/div[57]/ol/li[1]/span[2]/cite"
        return ref