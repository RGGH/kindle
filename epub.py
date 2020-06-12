#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+#
'''|r|e|d|a|n|d|g|r|e|e|n|.|c|o|.|u|k|'''
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+#
''' Downloads epub books and Converts
    ePUB to MOBI ready for your KINDLE
    Please download responsibly and donate'''

import requests
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
from pprint import pprint
import xlsxwriter
import glob
#
#
# Enter your URL here, code will do the rest #
# Base url should begin with "https://www.epubbooks.com/search?"
base_url = "https://www.epubbooks.com"
#
query  = urlparse('https://www.epubbooks.com/search?utf8=%E2%9C%93&q=huxley')
#
scheme = query.scheme # https
netloc = query.netloc # www.epubbooks.com
path = query.path # /search
#
query_str =  (query.query) # utf8=%E2%9C%93&q=huxley
params = parse_qs(query_str) # {'utf8': ['✓'], 'q': ['huxley']}
#
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0'
}
#
pubs=[]
# Make request - get the search results of the Author we want
res = requests.get("https://www.epubbooks.com/search?", params=params)
data = res.text

#  Use BS to get the title, link , and description of each book
soup  = BeautifulSoup(data,'html5lib')
#
for row in soup.findAll('li',attrs = {'class':'media'}):

    # Make a dictionary per book
    pub = {}

    # get title
    pub['title'] = row.text.strip().split("\n")[0].replace("Aldous Huxley", "").strip()

    # get image
    src = row.find(alt="thumbnail").get('src')
    pub['img'] = src
    # save image
    r = requests.get(src)
    open(pub['title'] +".jpg", 'wb').write(r.content)
    #
    # get link
    pub['link'] = row.a['href']
    if "book" in pub['link'] :
        pubs.append(pub)

# Show what we have available to put in CSV / XLSX file
pprint(pubs)

#------------------------------------- XL Shizz ---------------#
# Make xlsx file
workbook = xlsxwriter.Workbook("bookimages.xlsx")
worksheet = workbook.add_worksheet()

worksheet.set_column('E1:E5',7)
worksheet.set_default_row(40)


images = [filename for filename in glob.iglob('*.jpg', recursive=True)]
images = sorted(images)

# insert images (Book Cover Images)
image_row = 0
image_col = 0
for image in images:
    worksheet.insert_image(image_row,
                           image_col,
                           image,
                           {'x_scale':0.5,'y_scale':0.5,
                            'x_offset' : 0.5, 'y_offset':0.5,
                            'positioning':1})
    image_row +=1

titles = ([title['title'] for title in pubs])
titles = sorted(titles)
#print(title)

title_row = 0
title_col = 2

for title in titles:
    worksheet.write(title_row,
                    title_col,
                    title)
    title_row +=1

workbook.close()
