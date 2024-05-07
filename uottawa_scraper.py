# Web Scraper for course registry at the University of Ottawa
# Content taken from https://catalogue.uottawa.ca/en/courses/

import requests
from bs4 import BeautifulSoup
import json

# Format
json_format = {
    'course_id': {
        'course_name': 'course_name',
        'description': 'description',
        'prerequisites': 'string',
        'exclusions': 'string',
        'link': 'link'
    }
}

course_data = {}

URL = "https://catalogue.uottawa.ca/en/courses/"

page = requests.get(URL)
print("Done fetching homepage data")
soup = BeautifulSoup(page.content, "html.parser")

content = soup.find('div', class_ = 'az_sitemap')
blocks = content.find_all('ul')
blocks.pop(0)

links = []

for block in blocks:

    lists = block.find_all('a')

    for list in lists:

        code = list.get('href')
        links.append(code[-4:-1])

for link in links:

    page = requests.get("https://catalogue.uottawa.ca/en/courses/" + link + "/")
    print("Done fetching course data")
    soup = BeautifulSoup(page.content, "html.parser")

    course_blocks = soup.find_all('div', class_ = 'courseblock')

    for course_block in course_blocks:
        
        try:
            # title = course_block.find('p', class_ = 'courseblocktitle noindent')
            title = course_block.find('p', class_ = 'courseblocktitle noindent').get_text()
        except:
            title = ''
            print("Error getting title")
            # print(course_blocks.get_text())

        try:
            # desc = course_block.find('p', class_ = 'courseblockdesc noindent')
            desc = course_block.find('p', class_ = 'courseblockdesc noindent').get_text()
        except:
            desc = ''
            print("Error getting description")
            # print(course_blocks.get_text())

        try:
            prereq = course_block.find('p', class_ = 'courseblockextra highlight noindent').get_text()
        except:
            prereq = ''

        course_data[title] = {
            'title': title,
            'description': desc,
            'prereq': prereq
        }

        # course_id = title.split()[:2]

out_file = open("uottawa_course_data_raw.json", "w")
json.dump(course_data, out_file, indent = 6) 
out_file.close() 