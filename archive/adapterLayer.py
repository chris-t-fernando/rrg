from appLayer import sectorUseCases
from pprint import pprint


class adapterRDS():
    def __init(self):
# class needs to extend services 
# needs to load all the data in



        appLayer = sectorUseCases()

        searchTickers = [ 'xej', 'xmj' ]
        searchDateStart = '2021-02-01'
        searchDateEnd = '2021-02-21'
        xejInFeb = appLayer.newgetSectorQuotesBetweenDates(searchTickers, searchDateStart, searchDateEnd)

        for q in xejInFeb:
            for d in xejInFeb[q]:
                print(q + ' on ' + d + ': %s',xejInFeb[q][d])

        #sectors = appLayer.getSectors()
        #for k in sectors:
        #    print(k)

        #print(appLayer.getAllTickersInSector('xEj'))

        #print(appLayer.getTickersSector([ 'jpr' , 'DOR' ]))

class adapterJSON():
    pass

