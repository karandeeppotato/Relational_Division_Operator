from typing import Any
import tabulate
import pandas as pd
import tkinter as tk
from tkinter import *
import tkinter.ttk as ttk
import csv

student_data: dict[str, list[Any]] = {"Name": ["A", "B", "A", "C"], "Course": ["c1", "c1", "c2", "c2"]}
course_data: dict[str, list[Any]] = {"Course": ["c1", "c2"]}
after_division_data: dict[str, list[Any]] = {"Name": []}


class UpdateTable:
    @staticmethod
    def update_s_table(name, course):
        student_name = name
        student_course_name = course
        valid_course = False
        for i in course_data["Course"]:
            if student_course_name == i:
                valid_course = True
                student_data["Name"].append(student_name)
                student_data["Course"].append(student_course_name)
                student_df = pd.DataFrame(student_data)
                student_df.to_csv('student_data.csv', index=False)
                UI.confirmation_msg_true()
                break
            else:
                pass

        if not valid_course:
            UI.confirmation_msg_false()
            pass

    @staticmethod
    def update_c_table(course):
        course_name = course
        redundant_course = 0
        for i in course_data["Course"]:
            if course_name == i:
                UI.confirmation_msg_repeat()
                break
            else:
                redundant_course = 1

        if redundant_course == 1:
            course_data["Course"].append(course_name)
            course_df = pd.DataFrame(course_data)
            course_df.to_csv('course_data.csv', index=False)
            UI.confirmation_msg_true()
            pass


class PerformDivisionOperation:
    @staticmethod
    def operation():
        name_str = ["Name"]
        student_df = pd.read_csv('student_data.csv')
        student_dict = student_df.to_dict('list')
        course_df = pd.read_csv('course_data.csv')
        course_dict = course_df.to_dict('list')
        s_name = list(set(student_dict["Name"]))
        print("Unique Table : ")
        print(tabulate.tabulate(s_name, headers=name_str, tablefmt="fancy_grid"))

        c_name = course_dict["Course"]
        cross_product = [{a: b} for a in s_name for b in c_name]
        cross_headers = ["Name and Course"]
        cross_table = []
        for i in cross_product:
            cross_table.append(list(i.items()))
        print("Cross Product Table : ")
        print(tabulate.tabulate(cross_table, headers=cross_headers, tablefmt="fancy_grid"))

        s_name_not_set = student_dict["Name"]
        s_c_name = student_dict["Course"]
        st_product = [{s_name_not_set[i]: s_c_name[i]} for i in range(len(s_name_not_set))]
        cross_st_diff = [i for i in cross_product if i not in st_product]
        cross_st_name_diff = list()
        for i in range(len(cross_st_diff)):
            cross_st_name_diff.append(list(cross_st_diff[i].keys()))
        list_cross_st_name_diff = set()
        for i in range(len(s_name)):
            for j in range(len(cross_st_name_diff)):
                if s_name[i] == cross_st_name_diff[j][0]:
                    list_cross_st_name_diff.add(s_name[i])
        difference_table_header = ["Name"]
        print("Difference Table : ")
        print(tabulate.tabulate(list_cross_st_name_diff, headers=difference_table_header, tablefmt="fancy_grid"))

        s_name = set(s_name)
        final_result = s_name - list_cross_st_name_diff
        final_result = list(final_result)
        print("Final Result : ")
        print(tabulate.tabulate(final_result, headers=difference_table_header, tablefmt="fancy_grid"))
        for i in final_result:
            after_division_data["Name"].append(i)
        after_division_df = pd.DataFrame(after_division_data)
        after_division_df.to_csv("after_division_data.csv", index=False)


class UI:
    @staticmethod
    def menu():
        main_menu = Tk()
        main_menu.title("Division Operation")
        main_menu.geometry("700x400")
        main_menu.config(bg='#345B63')
        favicon = PhotoImage(file="icon/divide.png")
        main_menu.iconphoto(False, favicon)

        intro_label = Label(main_menu, text='Python based Relational Division Operation', width=57, height=2,
                            fg='black', bg='#D4ECDD',
                            relief=tk.FLAT, borderwidth=6)
        intro_label.config(font=('Helvetica', 15, 'bold'))
        intro_label.place(relx=0.5, rely=0.1, anchor=CENTER)

        perform_division_button = Button(main_menu, text=' Click to Perform Division Operation ', fg="white",
                                         bg="#152D35", command=UI.perform_division_ui)
        perform_division_button.config(font=('Helvetica', 10, 'bold'))
        perform_division_button.place(relx=0.5, rely=0.4, anchor=CENTER)

        show_relation_button = Button(main_menu, text='Click to view the relations ', fg="white",
                                      bg="#152D35", command=UI.show_data)
        show_relation_button.config(font=('Helvetica', 10, 'bold'))
        show_relation_button.place(relx=0.5, rely=0.6, anchor=CENTER)

        edit_relation_button = Button(main_menu, text='Click to edit the relations ', fg="white",
                                      bg="#152D35", command=UI.edit_table)
        edit_relation_button.config(font=('Helvetica', 10, 'bold'))
        edit_relation_button.place(relx=0.5, rely=0.8, anchor=CENTER)

        main_menu.mainloop()

    @staticmethod
    def perform_division_ui():
        perform_division_menu = Tk()
        perform_division_menu.title("Division Operation")
        perform_division_menu.config(bg='#345B63')
        width = 500
        height = 200
        screen_width = perform_division_menu.winfo_screenwidth()
        screen_height = perform_division_menu.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        perform_division_menu.geometry("%dx%d+%d+%d" % (width, height, x, y))
        perform_division_menu.resizable(0, 0)

        TableMargin = Frame(perform_division_menu, width=200)
        TableMargin.pack(side=TOP)
        scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
        scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
        tree = ttk.Treeview(TableMargin, columns="Name", height=400,
                            selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
        scrollbary.config(command=tree.yview)
        scrollbary.pack(side=RIGHT, fill=Y)
        scrollbarx.config(command=tree.xview)
        scrollbarx.pack(side=BOTTOM, fill=X)
        tree.heading('Name', text="Name", anchor=W)
        tree.column('#0', stretch=NO, minwidth=0, width=0)
        tree.pack()

        with open('after_division_data.csv') as f:
            reader = csv.DictReader(f, delimiter=',')
            for row in reader:
                Name = row['Name']
                tree.insert("", 0, values=Name)

    @staticmethod
    def show_data():
        show_data_menu = Tk()
        show_data_menu.title("Division Operation")
        show_data_menu.geometry("700x400")
        show_data_menu.config(bg='#345B63')

        intro_label = Label(show_data_menu, text='Select a relation', width=30, height=2, fg='black', bg='#D4ECDD',
                            relief=tk.FLAT, borderwidth=5)
        intro_label.config(font=('Helvetica', 15, 'bold'))
        intro_label.place(relx=0.5, rely=0.2, anchor=CENTER)

        show_student_data_button = Button(show_data_menu, text='Student Data', fg='white', bg='#152D35',
                                          command=UI.show_student_data)
        show_student_data_button.config(font=('Helvetica', 10, 'bold'))
        show_student_data_button.place(relx=0.5, rely=0.4, anchor=CENTER)

        show_course_data_button = Button(show_data_menu, text='Course Data', fg='white', bg='#152D35',
                                         command=UI.show_course_data)
        show_course_data_button.config(font=('Helvetica', 10, 'bold'))
        show_course_data_button.place(relx=0.5, rely=0.6, anchor=CENTER)

    @staticmethod
    def show_student_data():
        student_data_window = Tk()
        student_data_window.title("Division Operation")
        student_data_window.config(bg='#345B63')
        width = 500
        height = 200
        screen_width = student_data_window.winfo_screenwidth()
        screen_height = student_data_window.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        student_data_window.geometry("%dx%d+%d+%d" % (width, height, x, y))
        student_data_window.resizable(0, 0)

        TableMargin = Frame(student_data_window, width=200)
        TableMargin.pack(side=TOP)
        scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
        scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
        tree = ttk.Treeview(TableMargin, columns=("Name", "Course"), height=400,
                            selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
        scrollbary.config(command=tree.yview)
        scrollbary.pack(side=RIGHT, fill=Y)
        scrollbarx.config(command=tree.xview)
        scrollbarx.pack(side=BOTTOM, fill=X)
        tree.heading('Name', text="Name", anchor=W)
        tree.heading('Course', text="Course", anchor=W)
        tree.column('#0', stretch=NO, minwidth=0, width=0)
        tree.column('#0', stretch=NO, minwidth=0, width=0)
        tree.pack()

        with open('student_data.csv') as f:
            reader = csv.DictReader(f, delimiter=',')
            for row in reader:
                Name = row['Name']
                Course = row['Course']
                tree.insert("", 0, values=(Name, Course))

    @staticmethod
    def show_course_data():
        course_data_window = Tk()
        course_data_window.title("Division Operation")
        course_data_window.config(bg='#345B63')
        width = 500
        height = 200
        screen_width = course_data_window.winfo_screenwidth()
        screen_height = course_data_window.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        course_data_window.geometry("%dx%d+%d+%d" % (width, height, x, y))
        course_data_window.resizable(0, 0)

        TableMargin = Frame(course_data_window, width=200)
        TableMargin.pack(side=TOP)
        scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
        scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
        tree = ttk.Treeview(TableMargin, columns="Course", height=400,
                            selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
        scrollbary.config(command=tree.yview)
        scrollbary.pack(side=RIGHT, fill=Y)
        scrollbarx.config(command=tree.xview)
        scrollbarx.pack(side=BOTTOM, fill=X)
        tree.heading('Course', text="Course", anchor=W)
        tree.column('#0', stretch=NO, minwidth=0, width=0)
        tree.pack()

        with open('course_data.csv') as f:
            reader = csv.DictReader(f, delimiter=',')
            for row in reader:
                Course = row['Course']
                tree.insert("", 0, values=Course)

    @staticmethod
    def edit_table():
        edit_table_menu = Tk()
        edit_table_menu.title("Division Operation")
        edit_table_menu.geometry("700x400")
        edit_table_menu.config(bg='#345B63')

        intro_label = Label(edit_table_menu, text='Select a relation', width=30, height=2, fg='black', bg='#D4ECDD',
                            relief=tk.FLAT, borderwidth=5)
        intro_label.config(font=('Helvetica', 15, 'bold'))
        intro_label.place(relx=0.5, rely=0.2, anchor=CENTER)

        show_student_data_button = Button(edit_table_menu, text='Student Data', fg='white', bg='#152D35',
                                          command=UI.edit_student_table)
        show_student_data_button.config(font=('Helvetica', 10, 'bold'))
        show_student_data_button.place(relx=0.5, rely=0.4, anchor=CENTER)

        show_course_data_button = Button(edit_table_menu, text='Course Data', fg='white', bg='#152D35',
                                         command=UI.edit_course_table)
        show_course_data_button.config(font=('Helvetica', 10, 'bold'))
        show_course_data_button.place(relx=0.5, rely=0.6, anchor=CENTER)

    @staticmethod
    def edit_student_table():
        edit_student_table_menu = Tk()
        edit_student_table_menu.title("Division Operation")
        edit_student_table_menu.geometry("700x400")
        edit_student_table_menu.config(bg='#345B63')

        def submit_est_data():
            name_entry = edit_name_entry.get()
            course_entry = edit_course_entry.get()
            UpdateTable.update_s_table(name_entry, course_entry)

        intro_label = Label(edit_student_table_menu, text=' Enter name and course of the student ', width=35, height=2,
                            fg='black', bg='#D4ECDD', relief=tk.FLAT, borderwidth=5)
        intro_label.config(font=('Helvetica', 15, 'bold'))
        intro_label.place(relx=0.5, rely=0.2, anchor=CENTER)

        Label(edit_student_table_menu, text='Enter Name : ', fg='white', bg='#112031').place(relx=0.2, rely=0.45,
                                                                                             anchor=CENTER)
        edit_name_entry = Entry(edit_student_table_menu, bd=3, relief=tk.SUNKEN, justify=tk.CENTER)
        edit_name_entry.place(relx=0.4, rely=0.45, anchor=CENTER)

        Label(edit_student_table_menu, text='Enter Course : ', fg='white', bg='#112031').place(relx=0.2, rely=0.6,
                                                                                               anchor=CENTER)
        edit_course_entry = Entry(edit_student_table_menu, bd=3, relief=tk.SUNKEN, justify=tk.CENTER)
        edit_course_entry.place(relx=0.4, rely=0.6, anchor=CENTER)

        est_submit_button = Button(edit_student_table_menu, text='SUBMIT', fg='white', bg='#152D35',
                                   command=submit_est_data)
        est_submit_button.config(font=('Helvetica', 10, 'bold'))
        est_submit_button.place(relx=0.7, rely=0.5, anchor=CENTER)

    @staticmethod
    def edit_course_table():
        edit_course_table_menu = Tk()
        edit_course_table_menu.title("Division Operator")
        edit_course_table_menu.geometry("700x400")
        edit_course_table_menu.config(bg='#345B63')

        def submit_ect_data():
            new_course_data = edit_course_entry.get()
            UpdateTable.update_c_table(new_course_data)

        intro_label = Label(edit_course_table_menu, text=' Enter a new course ', width=35, height=2,
                            fg='black', bg='#D4ECDD', relief=tk.FLAT, borderwidth=5)
        intro_label.config(font=('Helvetica', 15, 'bold'))
        intro_label.place(relx=0.5, rely=0.2, anchor=CENTER)

        Label(edit_course_table_menu, text='Enter Course : ', fg='white', bg='#112031').place(relx=0.2, rely=0.6,
                                                                                              anchor=CENTER)
        edit_course_entry = Entry(edit_course_table_menu, bd=3, relief=tk.SUNKEN, justify=tk.CENTER)
        edit_course_entry.place(relx=0.4, rely=0.6, anchor=CENTER)

        ect_submit_button = Button(edit_course_table_menu, text='SUBMIT', fg='white', bg='#152D35',
                                   command=submit_ect_data)
        ect_submit_button.config(font=('Helvetica', 10, 'bold'))
        ect_submit_button.place(relx=0.7, rely=0.6, anchor=CENTER)

    @staticmethod
    def confirmation_msg_true():
        confirm_msg_window = Tk()
        confirm_msg_window.title("Process Successful")
        confirm_msg_window.geometry("700x80")
        confirm_msg_window.config(bg='#345B63')

        confirm_label = Label(confirm_msg_window, text="Value(s) updated successfully",
                              fg="Black", bg='#D4ECDD')
        confirm_label.place(relx=0.5, rely=0.5, anchor=CENTER)

    @staticmethod
    def confirmation_msg_false():
        not_confirm_window = Tk()
        not_confirm_window.title("Error")
        not_confirm_window.geometry("700x80")
        not_confirm_window.config(bg='#345B63')

        confirm_label = Label(not_confirm_window, text="The entered course is not present in course data !",
                              fg="Red", bg='#D4ECDD')
        confirm_label.place(relx=0.5, rely=0.5, anchor=CENTER)

    @staticmethod
    def confirmation_msg_repeat():
        not_confirm_window = Tk()
        not_confirm_window.title("Error")
        not_confirm_window.geometry("700x80")
        not_confirm_window.config(bg='#345B63')

        confirm_label = Label(not_confirm_window, text="The entered course is already present in the course data",
                              fg="Red", bg='#D4ECDD')
        confirm_label.place(relx=0.5, rely=0.5, anchor=CENTER)


PerformDivisionOperation.operation()
UI.menu()
