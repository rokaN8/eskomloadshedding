from urllib.request import urlopen
import datetime
from bs4 import BeautifulSoup

class Webscraper():

    def get_loadshedding_status(self):
        page = urlopen("http://loadshedding.eskom.co.za/LoadShedding/getstatus")
        soup = BeautifulSoup(page, "html.parser")
        print()
        status = int(str(soup)) - 1

        print("Current Status @", datetime.datetime.now(), "is Stage:", status)
        return status