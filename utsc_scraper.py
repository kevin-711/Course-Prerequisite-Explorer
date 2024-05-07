# Web Scraper for course registry at the University of Toronto Scarborough Campus
# Content taken from https://utsc.calendar.utoronto.ca/search-courses

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
# Handle prerequisits and exclusions and format them properly into lists later

course_data = {}

# Works on all course registrys of similar format, including those for UofT St George Campus
URL = "https://utsc.calendar.utoronto.ca/print/view/pdf/search_courses/print_page/debug"

page = requests.get(URL)
print("Done fetching data")
soup = BeautifulSoup(page.content, "html.parser")

courses = soup.find_all("div", class_ = "no-break w3-row views-row")

for course in courses:

    title = course.find('h3').text.split(':')
    course_id = title[0].strip()
    course_name = title[1].strip()

    description = course.find('p').text

    try:
        prerequisites_elem = course.find('span', class_ = 'views-field views-field-field-prerequisite')
        prerequisites = prerequisites_elem.find('span', class_ = 'field-content').get_text()
    except:
        prerequisites = ''
    
    try:
        exclusions_elem = course.find('span', class_ = 'views-field views-field-field-exclusion')
        exclusions = exclusions_elem.find('span', class_ = 'field-content').get_text()
    except:
        exclusions = ''

    link_elem = course.find('div', class_ = 'views-field views-field-field-timetable-link')
    link = link_elem.find('a').get('href').strip()

    course_data[course_id] = {
        'course_name': course_name,
        'description': description,
        'prerequisites': prerequisites,
        'exclusions': exclusions,
        'link': link
    }

out_file = open("utsc_course_data_raw.json", "w")
json.dump(course_data, out_file, indent = 6) 
out_file.close() 