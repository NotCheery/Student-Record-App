from tkinter import Tk, Entry, Text, END, font, Label, Button, BOTH
import sqlite3
from tkinter.messagebox import showinfo
from datetime import datetime

# Create the main application window
app = Tk()
app.title('Student Records')
app.geometry('600x600')

# Create a custom font with your desired size and other attributes
custom_font = font.nametofont("TkDefaultFont")  # Start with the default font
custom_font.configure(size=18)  # Set the desired font size

# Set the custom font as the default font for the application
app.option_add("*Font", custom_font)

# Connect to the SQLite database and create a cursor
conn = sqlite3.connect('records.db')
cursor = conn.cursor()

# Create a 'students' table in the database if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS students (pantherid INTEGER PRIMARY KEY, name TEXT, email TEXT)''')
conn.commit()

# Create and place labels for PantherID, Name, and Email
pantherid_label = Label(master=app, text='PantherID')
pantherid_label.grid(row=0, column=0)
name_label = Label(master=app, text='Name')
name_label.grid(row=1, column=0)
email_label = Label(master=app, text='Email')
email_label.grid(row=2, column=0)

# Create and place entry widgets for PantherID, Name, and Email
pantherid_entry = Entry(master=app)
pantherid_entry.grid(row=0, column=1)
name_entry = Entry(master=app)
name_entry.grid(row=1, column=1)
email_entry = Entry(master=app)
email_entry.grid(row=2, column=1)

# Define a function to handle adding a student record
def on_add_student_button_clicked():
    # Step-1: Obtain info from entry widgets
    pantherid = int(pantherid_entry.get())
    name = name_entry.get()
    email = email_entry.get()

    # Step-2: Insert these info into the database
    cursor.execute('INSERT INTO Students (PantherID, Name, Email) VALUES (?,?,?)', (pantherid, name, email))
    conn.commit()

    # Clear the entry fields
    pantherid_entry.delete(0, END)
    name_entry.delete(0, END)
    email_entry.delete(0, END)

    # Show an information message
    showinfo(message='Student record added to the database...')

# Define a function to list student records
def on_list_student_button_clicked():
    cursor.execute('SELECT * from Students')
    records = cursor.fetchall()
    txt.delete(0.0, END)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    txt.insert(END, f'--- Student list as of {timestamp} ---\n')
    for record in records:
        txt.insert(END, f"PantherID: {record[0]}   Name:{record[1]}   Email:{record[2]}\n")

# Create buttons for adding and listing student records
button_add = Button(master=app, text='Add Student', command=on_add_student_button_clicked)
button_add.grid(row=3, column=0, columnspan=1)

button_list = Button(master=app, text='List Students', command=on_list_student_button_clicked)
button_list.grid(row=4, column=0, columnspan=1)

# Create a Text widget to display student records
txt = Text(master=app, height=10, width=50)
txt.grid(row=10, column=0, columnspan=5) #changed the grid of text widget


'''My Code For Homework 5'''
'''When you update or delete a record, please click on student list button to see the changes'''

'''SEARCH RECORD'''
def search_record():
    try:
        pantherid = int(pantherid_entry.get()) #obtain pantherid from entry widget
    except:
        showinfo(message = f'Please enter a PantherID to search for a record') #if blank, then this message pops up
        
    pantherid_entry.delete(0, END) #clears entry box
    cursor.execute("SELECT * from Students WHERE pantherid = ?", (pantherid,)) #selects the record based on pantherid input
    records = cursor.fetchall() #pantherid number is assigned to the variable record
    
    if records: #checks to see if pantherid in records
        for record in records: 
            txt.insert(END, f'--- Student record ---\n')
            txt.insert(END, f"PantherID: {record[0]}   Name:{record[1]}   Email:{record[2]}\n")
    elif not records: #this message pops up if record for pantherid is not found
        showinfo(message = f'No record was found for {pantherid}\n')

#created button for finding student records
button_add = Button(master=app, text='Search Record', command=search_record)
button_add.grid(row=3, column=1, columnspan=1)


'''UPDATE RECORD'''
def update_record():
    
    try:
        #gets pantherid, name, email
        pantherid = int(pantherid_entry.get())
        name = name_entry.get()
        email = email_entry.get()
        
        if not pantherid or not name or not email: #shows this message if not ALL blanks are filled
            showinfo(message=f"Please enter PantherID, Name, and Email to update a record.")
            return #if not all blanks are filled, it stops further execution

        #clear entry boxes for all 3
        pantherid_entry.delete(0, END)
        name_entry.delete(0, END)
        email_entry.delete(0, END)
    
        cursor.execute("SELECT * from Students WHERE pantherid = ?", (pantherid,)) #selects the record based on pantherid input
        records = cursor.fetchall() #pantherid number is assigned to the variable record
    
        if records: # checks if pantherid exists in records
            cursor.execute("UPDATE Students SET email=?, name=? WHERE pantherid = ?", (email, name, pantherid))
            conn.commit() #makes sure the changes to the data is permanent
        else:
            showinfo(message= f'No record was found for {pantherid}.\n') #if pantherid not exist, this message pops up
            
    except: #same message shows up if ALL blanks are not filled. This is to prevent two pop-up messages at the same time
        showinfo(message=f"Please enter PantherID, Name, and Email to update a record.")
        

#Create button to update record
button_update = Button(master=app, text='Update Record', command=update_record) #calls to update_record function
button_update.grid(row=3, column=2, columnspan=4)

'''DELETE RECORD'''
def delete_record():
    try:
        pantherid = int(pantherid_entry.get()) #obtain pantherid from entry widget
    except:
        showinfo(message = f'Please enter a PantherID to delete a record')
    
    pantherid_entry.delete(0, END) #clears entry box
    cursor.execute("SELECT * from Students WHERE pantherid = ?", (pantherid,)) #selects the record based on pantherid input
    records = cursor.fetchall() #pantherid number is assigned to the variable records
    
    if records: #checks to see if pantherid in records exist
        cursor.execute("DELETE from students WHERE pantherid=?", (pantherid,)) #deletes record
        conn.commit() #permanatly deletes the record
        showinfo(message=f'Record for PantherID:{pantherid} deleted.')
    else:
        showinfo(message=f'No record was found for {pantherid}.')
        
#created a delete record button
delete_rec = Button(master=app, text='Delete Record', command=delete_record)
delete_rec.grid(row=4, column=1, columnspan=1)

'''EXPORT TO CSV'''
import csv
def export_csv():
    
    cursor.execute("SELECT * from Students") #selects data that will be exported
    
    csv_file = "‪students.csv" #created csv file
    
    with open(csv_file, 'w') as csvfile: #opens csv file in write mode
        write = csv.writer(csvfile)
        
        write.writerows(cursor) #write datarows to csv file
    
    #This helps find where the students.csv file is (seems to be exported to excel)
    import os
    print("Current Working Directory:", os.getcwd())

    #close connection
    conn.close()

#Button created for export to csv
csv_button = Button(master=app, text='Export to CSV', command=export_csv)
csv_button.grid(row=4, column=2, columnspan=1)

# Start the main application loop
app.mainloop()
