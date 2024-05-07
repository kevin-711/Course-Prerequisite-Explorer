import json

# Format
json_format = {
    'course_id': {
        'course_name': 'course_name',
        'description': 'description',
        'prerequisites': ['prerequisites list of lists'],
        'exclusions': ['exclusion1', 'exclusion2']
    }
}

file = open('utsc_course_data_raw.json')
course_data_raw = json.load(file)


# Problem with some prereqs with different formats (using ',' as delimeter instead of and)
def format_prereqs(key: str) -> list[list[str]]:
    
    prereqisites = []

    raw_prereqs = course_data_raw[key]['prerequisites']

    for char in '[]{}()/,.':
        raw_prereqs = raw_prereqs.replace(char, ' ')
    
    raw_prereqs = raw_prereqs.split('and')
    
    for prereqs in raw_prereqs:
        prereqs_list = []
        prereqs = prereqs.split()

        for prereq in prereqs:
            if prereq.isupper() and len(prereq) >= 6:
                prereqs_list.append(prereq)

        if prereqs_list:
            prereqisites.append(prereqs_list)

    return prereqisites



def format_exclusions(key: str) -> list[str]:

    exclusions = []

    raw_exclusions = course_data_raw[key]['exclusions']

    for char in '[]{}()/,.':
        raw_exclusions = raw_exclusions.replace(char, ' ')

    raw_exclusions = raw_exclusions.split()

    for exclusion in raw_exclusions:
        if exclusion.isupper() and len(exclusion) >= 6:
            exclusions.append(exclusion)

    return exclusions



# i = 0
for key in course_data_raw:

    course_data_raw[key]['prerequisites'] = format_prereqs(key)
    course_data_raw[key]['exclusions'] = format_exclusions(key)
    
    # print(i)
    # i += 1

# Honestly idk why these two values are different, final value of i is 2079, length is 2000
# print(len(course_data_raw))

out_file = open("utsc_course_data.json", "w")
json.dump(course_data_raw, out_file, indent = 4) 
out_file.close()

