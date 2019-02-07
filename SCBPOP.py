#Created by Richard Lo Sinno
import requests
import pandas as pd

class SCB:

    #Dictionary of region code and region names
    regions = {"00": "Riket", "01": "Stockholm", "03": "Uppsala", "04": "Södermanland",
               "05": "Östergötland","06": "Jönköping","07": "Kronoberg","08": "Kalmar",
               "09": "Gotland","10": "Blekinge","12": "Skåne", "13": "Halland", "14": "VGötaland",
               "17": "Värmland","18": "Örebro", "19": "Västmanland", "20": "Dalarna", "21": "Gävleborg",
               "22": "Västernorrland", "23": "Jämtland","24": "Västerbotten","25": "Norrbotten"}

    def __init__(self,region):
        region.sort()
        self.region = region

    def getPop(self):

        #Request URL
        url = "http://api.scb.se/OV0104/v1/doris/sv/ssd/BE/BE0101/BE0101A/BefolkningNy/"

        #Create query
        query = {"query": [
            {"code": "Region", "selection": {"filter": "item", "values": self.region}},
            {"code": "ContentsCode", "selection": {"filter": "item", "values": ["BE0101N1"]}}
        ], "response": {"format": "json"}}

        #Request the data
        r = requests.post(url, json=query)
        r.encoding = "utf-8-sig"
        result = r.json()['data']

        #Create return dict
        resDict = {'Year':[]}

        #Add regions
        for item in self.region:
            convertId = self.regions.get(item)
            resDict[convertId] = []

        # Add years and region data
        for item in result:
            convertId = self.regions.get(item['key'][0])
            if self.region[0] == item['key'][0]:
                resDict['Year'].append(int(item['key'][1]))
                resDict[convertId].append(int(item['values'][0]))
            else:
                resDict[convertId].append(int(item['values'][0]))


        #return Python dict
        return(resDict)

if __name__ == "__main__":

    #Region codes
    region = ["01","03","04","05","06","07","08","09","10","12","13","14","17","18","19","20","21","22","23","24","25"]

    #Request JSON data and return Python Dict
    result = SCB(region).getPop()

    #Print result
    print(result)



