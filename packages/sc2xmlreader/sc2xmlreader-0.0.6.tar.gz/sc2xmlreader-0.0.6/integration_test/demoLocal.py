
from sc2xmlreader_dev.sc2xmlreader import SC2XMLReader
from sc2xmlreader_dev.const import DEFAULT_USERNAME, DEFAULT_PASSWORD

import pprint

class LocalDemo:
    def __init__(self, url:str):
        self.remote = SC2XMLReader(url, DEFAULT_USERNAME, DEFAULT_PASSWORD)


    def ShowSystemInfo(self):
        pprint.pprint("""Manufacturer: {0}""".format(self.remote.manufacturer))
        pprint.pprint("""Systemnummer: {0}""".format(self.remote.data["number"]["Value"]))
        pprint.pprint("""Systemtype: {0}""".format(self.remote.data["type"]["Value"]))




if __name__ == '__main__':
    o = LocalDemo('http://solvis.leu.loc')

    o.ShowSystemInfo()