#from tickerQuote import tickerQuote

#aQuote = tickerQuote('avh', 'today', 10, 20, 5, 3, 4.99, 10000)

#print(aQuote.getQuote())

#import baseTickerObject
from tickerQuote import tickerQuote
from sectorQuote import sectorQuote
import logging, sys
from pprint import pprint
from datetime import datetime

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

# temporary until I use eventbridge to stitch it all together
# will then be pulled out and put into an adapter class
import csv

sectors = {}

# populate sectors, which is a Dict (key sector ticker) containing
# ['tickers'], which is a List of tickers belonging to this sector
# ['quotes'], which is a Dict of historical quotes for this ticker
# start with creating the object and populating ['tickers']
with open('sector-ticker-map.csv', newline='') as csvfile:
    mapReader = csv.DictReader(csvfile, delimiter=',')

    for row in mapReader:
        # if the sector key doesn't exist, create it
        if row['sector'] not in sectors:
            sectors[row['sector']] = {}
            sectors[row['sector']]['quotes'] = {}
            sectors[row['sector']]['tickers'] = []
            
        sectors[row['sector']]['tickers'].append(row)

# now populate the historical quotes
with open('sectors.csv', newline='') as csvfile:
    tickerReader = csv.DictReader(csvfile, delimiter=',')
    for row in tickerReader:
        #logging.debug("Adding row. Ticker %s, Date, %s, Close price %s, Open price %s, High price %s, Low price %s, Volume %s", row['ticker'], row['date'], row['close'], row['open'], row['high'], row['low'], row['volume'])
        # todo - I forgot to add 'offer'.  I don't think I'll use it but noting just in case.  hardcoding to 0 because I'm lazy
        sectors[row['sectorticker']]['quotes'][row['date']] = sectorQuote(row['sectorticker'], row['date'], row['open'], row['high'], row['low'], 0, row['close'], row['volume'])

def validateDate(theDate):
    try:
        return datetime.strptime(theDate, '%Y-%m-%d')

    except Exception as error:
        raise
        return False


# returns a list of SECTOR quotes (not individual ticker quotes)
# allSectors is the sectors data structure created above
# searchSectors is a List of the sectors to be queried.  An empty List means all tickers
# startDate and endDate are yyyy-mm-dd formatted dates
# returns a List of positions

def getSectorQuotesBetweenDates(allSectors, searchSectors, strStartDate, strEndDate):
    startDate = validateDate(strStartDate)
    endDate = validateDate(strEndDate)

    if ( startDate == False ) or ( endDate == False):
        raise ValueError('Start and end dates must be in YYYY-MM-DD format')

    if startDate > endDate:
        raise ValueError('End date must be after start date')
    
# todo: properly validate
#    try:
#        if ( type(allSectors['tickers']) != list ) or ( type(allSectors['quotes']) != dict ):
#            raise TypeError('First parameter must be a Dict containing a key labelled tickers that contains a List, and another key labelled quotes that contains a Dict')
#    except:
#        raise

    try:
        if type(searchSectors) != list:
            raise TypeError('Second parameter must be a List')
    except:
        raise

    # holds matched quotes
    # matchedQuotes['sectorName'][n] equals the dict key date in sectors['sectorName']['quotes'] of each match
    # matchedQuotes is a Dict
    # matchedQuotes['sectorName'] is a List
    matchedQuotes = {}

    # for each allSectors
    #   for each searchSectors
    #     does this allSectors == this searchSectors? or is searchSectors *?
    #       is the quote date equal to or within the search dates?
    #         if so, record this position
    #         if not, ignore
    for allSector in allSectors:
        for searchSector in searchSectors:
            if allSector == searchSector:
                # found a sector we're interested in
                matchedQuotes[allSector] = []
                for quote in allSectors[allSector]['quotes']:
                    # convert the key to a date
                    date_time_obj = datetime.strptime(quote, '%Y-%m-%d')

                    # is this date between the dates we're looking for
                    if ( date_time_obj >= startDate ) and ( date_time_obj <= endDate ):
                        # meets date criteria
                        matchedQuotes[allSector].append(quote)
                        
    return matchedQuotes

# just a wrapper for between dates
def getSectorQuotesOnDate(allSectors, searchSectors, searchDate):
    return getSectorQuotesBetweenDates(allSectors, searchSectors, searchDate, searchDate)

#print(getSectorQuotesBetweenDates(sectors, ['xej', 'xmj'], '2021-02-01', '2021-03-01'))

searchTickers = [ 'xej', 'xmj' ]
searchDateStart = '2021-02-01'
searchDateEnd = '2021-02-21'
xejInFeb = getSectorQuotesBetweenDates(sectors, searchTickers, searchDateStart, searchDateEnd)

for q in xejInFeb:
    for d in xejInFeb[q]:
        print(q + ' on ' + d + ': ' + sectors[q]['quotes'][d].getPriceHigh())


### Later - code to search for specific sectors AND specific tickers, to return the individual member ticker values
    # for each allSectors
    #   for each searchSectors
    #     does this allSectors == this searchSectors? or is searchSectors *?
    #     if so, for each allSectors-ticker
    #       for each searchTickers
    #         does this allSectors-ticker == this searchTickers or is searchTickers *?
    #           is the quote date equal to or within the search dates?
    #             if so, record this position
    #             if not, ignore
    # return an array that looks like
    # {
    #   'xej': {
    #     'quotes': {
    #       positionNumber
    #     }
    #   }
    # }

#    for allSector in allSectors:
#        for searchSector in searchSectors:
#            if allSector == searchSector:
#                tickersInThisSector = []
#                for searchTicker in searchTickers:
#                    for allTicker in allSectors[allSector]['tickers']:
#                        if allTicker['ticker'] == searchTicker:
#                            # now we know that searchTicker is in this sector
#                            # hold on to this ticker
#                            print(allTicker['ticker'])
#                            tickersInThisSector.append(allTicker['ticker'])
#                
#                # now we know which tickers are in this sector, we need to loop through the quotes
#                # a relational database would be pretty great for this job...
#                for quote in allSector['quotes']:
#                    # if the quote is for this