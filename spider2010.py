import bs4, re, urllib2, time, csv
from bs4 import BeautifulSoup


with open('data_2010.csv', 'wb') as out_f:
    outdata = csv.writer(out_f)
    outdata.writerow(['Province', 'District', 'Polling Division', 'Name',
                      'Votes', 'Percent'])
    
    # Pages are structured as
    # Table of province names with links to the districts within them
    #    Table of district names with links to the polling division in them
    #        Table of results in this division (name, vote total, percent)
    
    start = 'http://www.slelections.gov.lk/presidential2010/province.html'
    startpage = BeautifulSoup(urllib2.urlopen(start), 'lxml')
    links = startpage.findAll('table')[9]
    for row in links.findAll('tr')[3:12]: # Look through rows of the main table
        province = row.findAll('td')[0].text
        link = row.findAll('td')[1].find('a')['href']
        # Get full link to the districts in this province
        link = 'http://www.slelections.gov.lk/presidential2010/' + link
        # This page lists the districts within this province and links
        # to their polling divisions
        districtpage = BeautifulSoup(urllib2.urlopen(link), 'lxml')
        districtlinks = districtpage.findAll('table')[9]
        
        for drow in districtlinks.findAll('tr')[2:]: # Look through districts
            districtname = drow.findAll('td')[0].text
            # Get link to the polling divisions in this district
            dlink = drow.findAll('td')[1].find('a')['href']
            dlink = 'http://www.slelections.gov.lk/presidential2010/' + dlink
            divpage = BeautifulSoup(urllib2.urlopen(dlink), 'lxml')
            divlinks = divpage.findAll('table')[9]
            for divrow in divlinks.findAll('tr')[2:]: # Look through divisions
                divname = divrow.findAll('td')[0].text
                print province, districtname, divname
                divlink = divrow.findAll('td')[1].find('a')['href']
                divlink = 'http://www.slelections.gov.lk/presidential2010/' + \
                    divlink
                page = BeautifulSoup(urllib2.urlopen(divlink), 'lxml')
                data = page.findAll('table')[12]
                for prow in data.findAll('tr')[1:-1]: # Look at candidates
                    cells = prow.findAll('td')
                    name = cells[0].text.strip()
                    votes = cells[1].text.strip()
                    percent = cells[2].text.strip()
                    row = [province, districtname, divname, name, votes,
                           percent]
                    outdata.writerow(row)
            