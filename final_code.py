import requests
from bs4 import BeautifulSoup
import urllib.parse
import urllib.request
import re
import pandas as pd
 
url = "http://www16.co.hennepin.mn.us/pins/addrresult.jsp"
 
house = input ("Enter house :")
street = input ("Enter street :")

# Default values
# house = "4001"
# street = "DUPONT"

house = house.lower()
street = street.lower()

post_params = {'house': house,'street': street,'condo': '','ps': '50000','Submit': 'Search',}
post_args = urllib.parse.urlencode(post_params).encode("utf-8")
 
fp = urllib.request.urlopen(url, post_args)
soup2 = BeautifulSoup(fp,'lxml')

 
links = soup2.find_all('a')

val = []
for link in links:
	if "pidresult" in link.attrs['href']:
		if link.attrs['href'][0:31] not in val:
			val.append(link.attrs['href'][0:31])

cols2 = ['Property ID number:','Address:','Municipality:','School district:','Watershed:','Sewer district:','Construction year:','Owner name:','Taxpayer name & address:','Sale information','Sale date:','Sale price:','Transaction type:','Tax parcel description','Addition name:','Lot:','Block:','Approximate parcel size:','Metes & Bounds: Common abbreviations','Abstract or Torrens:','Estimated market value:','Taxable market value:','Total improvement amount:','Total net tax:','Total special assessments:','Solid waste fee:','Total Tax:','Land market:','Building market:','Machinery market:','Total market:','Qualifying improvements:','Veterans exclusion:','Homestead market value exclusion:','Property type:','Homestead status:','Relative homestead:','Agricultural:','Exempt status:']

df = pd.DataFrame(None,columns=cols2)
 
url2 = 'http://www16.co.hennepin.mn.us/pins/'
for i in val:
	temp_url = url2 + i
	print(temp_url)
	temp_soup = BeautifulSoup(requests.get(temp_url).content,'lxml')

	table = temp_soup.find('table',id="TABLE_DETAILS")
	table2 = temp_soup.find('table',id="Table_Detail")
	data = []
	rows = table.find_all('tr')
	rows2 = table2.find_all('tr')
	for row in rows:
		cols = row.find_all('td')
		cols = [ele.text.strip() for ele in cols]
		data.append([ele for ele in cols if ele])
	for row in rows2:
		cols = row.find_all('td')
		cols = [ele.text.strip() for ele in cols]
		data.append([ele for ele in cols if ele])

	df_temp = pd.DataFrame(data)
	df_temp = df_temp.replace('\n',' ', regex=True)
	df_temp = df_temp.replace('\r',' ', regex=True)
	df_temp = df_temp.replace('\t',' ', regex=True)
	df_temp = df_temp.replace('  +',' ', regex=True)
	df_temp2 = pd.DataFrame([list(df_temp[1])],columns = list(df_temp[0]))

	temp_list = []
	for col_name in cols2:
		if col_name in df_temp2.columns:
			temp_list.append(df_temp2[col_name][0])
		else:
			temp_list.append("Entry not found")

	df_temp2 = pd.DataFrame([temp_list],columns = cols2)
	df.loc[len(df)] = list(df_temp2.iloc[0])
# print(df)
street=re.sub(' ','_',street)
df.to_csv(house+'_'+street+'.csv',index=False)

