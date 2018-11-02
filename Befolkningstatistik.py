#Created by Richard Lo Sinno

import requests
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from matplotlib import style
style.use('bmh')

class SCB:

    query = {"query": [], "response": {"format": "json"}}
    result = None
    regions = {"00": "Riket", "01": "Stockholm", "03": "Uppsala", "04": "Södermanland", "05": "Östergötland","06": "Jönköping","07": "Kronoberg","08": "Kalmar","09": "Gotland","10": "Blekinge","12": "Skåne", "13": "Halland", "14": "VGötaland", "17": "Värmland","18": "Örebro", "19": "Västmanland", "20": "Dalarna", "21": "Gävleborg","22": "Västernorrland", "23": "Jämtland","24": "Västerbotten","25": "Norrbotten"}
    clean_df = {"Year": []}
    length_regions = 0
    length_dates = 0

    def __init__(self,url, region, content):
        self.url = url
        self.region = region
        self.content = content
        region = {"code":"Region", "selection":{"filter":"item","values":self.region}}
        content = {"code": "ContentsCode","selection": {"filter": "item","values":[self.content]}}
        self.query["query"].append(region)
        self.query["query"].append(content)

        for i in range(len(self.region)):
            self.clean_df[self.region[i]] = []
            self.length_regions += 1

    def req(self):
        r = requests.post(self.url, json=self.query)
        r.encoding = "utf-8-sig"
        self.result = pd.DataFrame(r.json()['data'])
        query.fixData()

    def fixData(self):

        #add dates
        control = self.result['key'][0][0]
        for item in self.result['key']:
            if item[0] == control:
                item[1] = int(item[1])
                self.clean_df['Year'].append(item[1])
                self.length_dates += 1

        #add values
        for i in range(self.length_regions):
            for item in self.result['values'][(self.length_dates * i):(self.length_dates * (i+1))]:
                self.clean_df[self.region[i]].append(int(item[0]))

        #create the new df
        self.result = pd.DataFrame(self.clean_df)

        # rename columns
        for i in range(self.length_regions):
            self.result.rename(columns={self.region[i]: self.regions.get(self.region[i])}, inplace=True)

        self.change()

    def change(self):
        for item in self.region:
            val = self.regions.get(item, item)
            self.result[val + " %"] = (self.result[val] - self.result[val][0])/self.result[val][0] *100
        self.print()

    def print(self):
        stats = self.result
        stats.set_index("Year", inplace=True)

        print(stats)

        for item in stats:
            if "%" in item:
                plt.subplot(211)
                plt.plot(stats.loc[:, item])
                plt.legend(loc='upper left')
                plt.title("Befolkningsförändring ")
                plt.ylabel("Förändring invånare %")
            else:
                plt.subplot(212)
                plt.plot(stats.loc[:, item]/ 1000)
                plt.legend(loc='upper left')
                plt.title("Befolkningsantal ")
                plt.ylabel("Antal invånare (1000-tal)")

        plt.show()

choice = pd.Series(SCB.regions)


quit = False
regionlist = []

#User interface
while quit == False:
    print(choice)
    value = input("Add a region by inputing the region code. When you are done input q to quit and get the stats. \n")
    if value.lower() == "q":
        quit = True
    elif value in choice.index:
        if not value in regionlist:
            regionlist.append(value)
        value = input(choice.get(value) + " was added to the list. Press enter to add another or q to quit and get the stats. \n")
        if value == "q":
            quit = True
    elif not value in choice.index:
        value = input("Wrong input, please try again by pushing enter or q to quit.\n")
        if value == "q":
            quit = True

regionlist.sort()
if len(regionlist) > 0:
    query = SCB("http://api.scb.se/OV0104/v1/doris/sv/ssd/BE/BE0101/BE0101A/BefolkningNy/", regionlist, "BE0101N1")
    query.req()
