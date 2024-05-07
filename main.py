# Driver for course viewer at UTSC
# Use scraper and formatter first to collect and parse course data

import json
import tkinter
import customtkinter

file = open('utsc_course_data.json')
course_data = json.load(file)

def get_prerequisites(key: str, prereqs: list[str]) -> list[str]:

    prereqs_list = course_data[key]['prerequisites']

    for prereq in prereqs_list:

        for req in prereq:
            if req in prereqs or req not in course_data:
                break
            if req not in prereqs:
                prereqs.append(req)
                prereqs = get_prerequisites(req, prereqs)
                break

    return prereqs


def format_prereq(course: dict) -> str:

    prerequisites = ''
    for prerequsite in course['prerequisites']:
        for prereq in prerequsite:
            prerequisites += prereq + '/'
        prerequisites = prerequisites[:-1]
        prerequisites += ' and '
    return prerequisites[:-5]


def format_exclusions(course: dict) -> str:
    
    exclusions = ''
    for exclusion in course['exclusions']:
        exclusions += exclusion + ', '
    return exclusions[:-2]


def get_info():

    course_code = entry.get().upper()
    entry.delete(0, 'end')

    if course_code in course_data:
        course = course_data[course_code]

        prerequisites = format_prereq(course)
        exclusions = format_exclusions(course)

        out_text = course_code + " - " + str(course['course_name']) \
        + "\n\nDescription:\n" + str(course['description'] ) \
        + '\n\nPrerequisites: ' + prerequisites \
        + '\n\nExclusions: ' + exclusions

        output.configure(text = out_text)

    else:
        output.configure(text = "Error, Course Code Not Found")


def get_all_prereqs():

    course_code = entry.get().upper()
    entry.delete(0, 'end')

    if course_code in course_data:
        course = course_data[course_code]
        prereqs = get_prerequisites(course_code, [])

        prerequisites = ''
        for prereq in prereqs:
            prerequisites += prereq + ', '
        prerequisites = prerequisites[:-2]

        out_text = course_code + " - " + str(course['course_name']) \
        + '\n\nAll Prerequisites: ' + prerequisites

        output.configure(text = out_text)

    else:
        output.configure(text = "Error, Course Code Not Found")
    


customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

root = customtkinter.CTk()
root.geometry("720x480")
root.title("Course Viewer")

title = customtkinter.CTkLabel(root, font = ("Times", 30, "bold"), text = "Course Viewer")
title.pack(padx = 15, pady = 15)

course_code = tkinter.StringVar()
entry = customtkinter.CTkEntry(root, placeholder_text="Enter Course Code", textvariable = course_code)
entry.pack(padx = 15, pady = 15)

info_btn = customtkinter.CTkButton(root, text = 'Get Course Info', corner_radius = 10, command = get_info)
info_btn.pack(padx = 5, pady = 5)

prereq_btn = customtkinter.CTkButton(root, text = 'Get All Prerequisites', corner_radius = 10, command = get_all_prereqs)
prereq_btn.pack(padx = 5, pady = 5)

output = customtkinter.CTkLabel(root, font = ("Times", 15, "bold"), text = '', wraplength = 600)
output.pack(padx = 15, pady = 15)

root.mainloop()