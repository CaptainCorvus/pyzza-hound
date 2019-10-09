import bs4 as bs
import requests
import urllib

schedule_url = 'http://mlb.mlb.com/mlb/schedule/index.jsp?tcid=mm_mlb_schedule#date=07/13/2019'

html = requests.get(schedule_url).content
soup = bs.BeautifulSoup(html, 'html.parser')

divs = soup.findAll('div')
schedule_container = ''
for d in divs:
    id = d.get('id', False)
    if not id:
        continue
    if id.lower() == 'schedulecontainer':
        schedule_container = d
        print("schedule_container!!")
    print()
print()
