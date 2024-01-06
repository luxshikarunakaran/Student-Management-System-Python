# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
# pip install mysql-connector-python



# MySQL connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="sms"
)

mycursor = mydb.cursor()




# Function to add student
def add_student():
    # get values from entry
    Roll_number = id_entry.get()
    Name = name_entry.get()
    Gender = gender_combobox.get()
    Age = age_entry.get()
    Contact = contact_entry.get()
    Grade = grade_combobox.get()

    # Check if all fields are filled
    if not all([Roll_number, Name, Gender, Age, Contact, Grade]):
        messagebox.showerror("Error", "All fields must be filled")
        return

    # Code for saving into the database
    try:
        # Your SQL query to insert data
        sql = "INSERT INTO students (Roll_number, Name, Gender, Age, Contact, Grade) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (Roll_number, Name, Gender, Age, Contact, Grade)

        mycursor.execute(sql, values)
        mydb.commit()

        messagebox.showinfo("Success", "Student added successfully")

        # Refresh the student table
        display_students()

    except Exception as e:
        # Handle any exceptions that may occur during the database operation
        messagebox.showerror("Error", f"An error occurred: {str(e)}")



# Function to display students in a table
def display_students():
    # Clear existing items in the treeview
    for i in student_tree.get_children():
        student_tree.delete(i)

    try:
        # Your SQL query to fetch student data
        sql = "SELECT * FROM students"
        mycursor.execute(sql)

        # Fetch all the records
        records = mycursor.fetchall()

        # Insert records into the treeview
        for record in records:
            student_tree.insert("", "end", values=record)

    except Exception as e:
        # Handle any exceptions that may occur during the database operation
        messagebox.showerror("Error", f"An error occurred: {str(e)}")



# Function to search for a student
def search_student():
    # get value from entry
    roll_number = search_entry.get()

    # Check if the search field is filled
    if not roll_number:
        messagebox.showerror("Error", "Enter Roll Number to search")
        return

    try:
        # Your SQL query to fetch student data
        sql = "SELECT * FROM students WHERE Roll_number = %s"
        values = (roll_number,)

        mycursor.execute(sql, values)
        records = mycursor.fetchall()

        # Clear existing items in the treeview
        for i in student_tree.get_children():
            student_tree.delete(i)

        # Insert records into the treeview
        for record in records:
            student_tree.insert("", "end", values=record)

    except Exception as e:
        # Handle any exceptions that may occur during the database operation
        messagebox.showerror("Error", f"An error occurred: {str(e)}")




# Function to delete a student
def delete_student():
    # get value from entry
    roll_number = search_entry.get()

    # Check if the search field is filled
    if not roll_number:
        messagebox.showerror("Error", "Enter Roll Number to delete")
        return

    try:
        # Your SQL query to delete student data
        sql = "DELETE FROM students WHERE Roll_number = %s"
        values = (roll_number,)

        mycursor.execute(sql, values)
        mydb.commit()

        messagebox.showinfo("Success", "Student deleted successfully")

        # Refresh the student table
        display_students()

    except Exception as e:
        # Handle any exceptions that may occur during the database operation
        messagebox.showerror("Error", f"An error occurred: {str(e)}")



# Function to update student details
def update_student():
    # get values from entry
    Roll_number = id_entry.get()
    Name = name_entry.get()
    Gender = gender_combobox.get()
    Age = age_entry.get()
    Contact = contact_entry.get()
    Grade = grade_combobox.get()

    # Roll number is required to update a student
    if not Roll_number:
        messagebox.showerror("Error", "Enter Roll Number to update")
        return

    try:
        # fetch particular student data from database
        sql = "SELECT * FROM students WHERE Roll_number = %s"
        values = (Roll_number,)
        mycursor.execute(sql, values)
        record = mycursor.fetchone()

        print(Grade)
        print(Gender)

        # Update the values if provided
        if record:
            if not Name:
                Name = record[1]
            if not Gender or gender_combobox.get() == "Select Gender":
                Gender = record[2]
            if not Age:
                Age = record[3]
            if not Contact:
                Contact = record[4]
            if not Grade or  grade_combobox.get() == "Select Grade":
                Grade = record[5]


        # Your SQL query to update data
        sql = "UPDATE students SET Name=%s, Gender=%s, Age=%s, Contact=%s, Grade=%s WHERE Roll_number=%s"
        values = (Name, Gender, Age, Contact, Grade, Roll_number)

        mycursor.execute(sql, values)
        mydb.commit()

        messagebox.showinfo("Success", "Student details updated successfully")

        # Refresh the student table
        display_students()

    except Exception as e:
        # Handle any exceptions that may occur during the database operation
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


# Function to clear Entry and reset Combobox
def clear_entry_and_combobox():
    id_entry.delete(0, END)
    name_entry.delete(0, END)
    gender_combobox.set("Select Gender")
    grade_combobox.set("Select Grade")
    age_entry.delete(0, END)
    contact_entry.delete(0, END)


# create desktop window -------------------------------------------------------------------------------------------------
root = Tk()
# set full screen width and height
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
# set title
root.title("Student Management System")
# set background color
root.config(bg="white")
# set resizable
root.resizable(True, True)

# set heading
title = Label(root, text="Student Management System", font=("times new roman", 40, "bold"), bg="white", fg="green")
title.grid(row=0, column=0, columnspan=2, sticky='ew')

# detail frame name "details"
details_frame = LabelFrame(root, text="Student Details", font=("Enter Details", 20, "bold"), bg="white", fg="green")
details_frame.grid(row=1, column=0, columnspan=2, sticky='nsew')

# label and entry for Roll Number
id_label = Label(details_frame, text="Student ID", font=("Roll Number", 15, "bold"), bg="white", fg="green", anchor='w')
id_label.grid(row=0, column=0, padx=20, pady=10, sticky='w')

id_entry = Entry(details_frame, font=("Name", 15))
id_entry.grid(row=0, column=1, padx=20, pady=10, sticky='w')

# label and entry for Name
name_label = Label(details_frame, text="Student Name", font=("Name", 15, "bold"), bg="white", fg="green", anchor='w')
name_label.grid(row=1, column=0, padx=20, pady=10, sticky='w')

name_entry = Entry(details_frame, font=("Name", 15))
name_entry.grid(row=1, column=1, padx=20, pady=10, sticky='w')

# label and entry for Gender
gender_label = Label(details_frame, text="Gender", font=("Name", 15, "bold"), bg="white", fg="green", anchor='w')
gender_label.grid(row=2, column=0, padx=20, pady=10, sticky='w')

gender_options = ["Male", "Female"]
gender_combobox = ttk.Combobox(details_frame, values=gender_options, font=("Name", 15), state="readonly")
gender_combobox.grid(row=2, column=1, padx=20, pady=10, sticky='w')
gender_combobox.set("Select Gender")

# label and entry for grade
grade_label = Label(details_frame, text="Grade", font=("Name", 15, "bold"), bg="white", fg="green", anchor='w')
grade_label.grid(row=3, column=0, padx=20, pady=10, sticky='w')

grade_options = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
grade_combobox = ttk.Combobox(details_frame, values=grade_options, font=("Name", 15), state="readonly")
grade_combobox.grid(row=3, column=1, padx=20, pady=10, sticky='w')
grade_combobox.set("Select Grade")

# label and entry for Age
age_label = Label(details_frame, text="Age", font=("Name", 15, "bold"), bg="white", fg="green", anchor='w')
age_label.grid(row=4, column=0, padx=20, pady=10, sticky='w')

age_entry = Entry(details_frame, font=("Name", 15))
age_entry.grid(row=4, column=1, padx=20, pady=10, sticky='w')

# label and entry for Contact
contact_label = Label(details_frame, text="Contact", font=("Name", 15, "bold"), bg="white", fg="green", anchor='w')
contact_label.grid(row=5, column=0, padx=20, pady=10, sticky='w')

contact_entry = Entry(details_frame, font=("Name", 15))
contact_entry.grid(row=5, column=1, padx=20, pady=10, sticky='w')

# button frame
btn_frame = Frame(details_frame, bg="white")
btn_frame.grid(row=6, column=0, columnspan=2, sticky='nsew')

# add button
add_btn = Button(btn_frame, text="Add", font=("times new roman", 15, "bold"), bg="green", fg="white", cursor="hand2", command=add_student)
add_btn.grid(row=0, column=0, padx=20, pady=10, sticky='w')

# view button
view_btn = Button(btn_frame, text="View", font=("times new roman", 15, "bold"), bg="green", fg="white", cursor="hand2", command=display_students)
view_btn.grid(row=0, column=1, padx=20, pady=10, sticky='w')

# delete button
delete_btn = Button(btn_frame, text="Delete", font=("times new roman", 15, "bold"), bg="green", fg="white", cursor="hand2", command=delete_student)
delete_btn.grid(row=0, column=2, padx=20, pady=10, sticky='w')

# update button
update_btn = Button(btn_frame, text="Update", font=("times new roman", 15, "bold"), bg="green", fg="white", cursor="hand2", command=update_student)
update_btn.grid(row=0, column=3, padx=20, pady=10, sticky='w')

# clear button
clear_btn = Button(btn_frame, text="Clear", font=("times new roman", 15, "bold"), bg="green", fg="white", cursor="hand2", command=clear_entry_and_combobox)
clear_btn.grid(row=0, column=4, padx=20, pady=10, sticky='w')


# search entry and button
search_entry = Entry(btn_frame, font=("Name", 15))
search_entry.grid(row=1, column=0, padx=20, pady=10, sticky='w')

search_btn = Button(btn_frame, text="Search", font=("times new roman", 15, "bold"), bg="green", fg="white", cursor="hand2", command=search_student)
search_btn.grid(row=1, column=1, padx=20, pady=10, sticky='w')

# configure row and column weights
for i in range(7):  # Adjust the range based on the number of rows
    details_frame.grid_rowconfigure(i, weight=1)
    details_frame.grid_columnconfigure(i, weight=1)





# create a treeview for displaying students
columns = ("Roll Number", "Name", "Gender", "Age", "Contact", "Grade")
student_tree = ttk.Treeview(root, columns=columns, show="headings", height=20)

# set column headings
for col in columns:
    student_tree.heading(col, text=col)
    student_tree.column(col, width=100)  # adjust width as needed

student_tree.grid(row=1, column=2, rowspan=7, padx=10, pady=10, sticky='nsew')

# configure row and column weights for the treeview
for i in range(7):
    root.grid_rowconfigure(i, weight=1)

root.grid_columnconfigure(2, weight=1)

# display initial student data
display_students()

root.mainloop()
