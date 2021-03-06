import requests
from tkinter import *
from socket import *
import json

sock = socket()
messages = []
EXIT = '[EXIT]'
request_msg = ""  # The user input or edit/create step
property_editing = ""
new_property_val = ""
student_index = ""
new_fname = ""
new_lname = ""
new_grade = ""
new_major = ""


def message_entry_event_handler(event):
    """Initiate a request when the user presses enter"""
    if event.char == "\r":
        initiate_request()


def client_id_entry_handler(event):
    """Connect when the user presses enter """
    if event.char == "\r":
        connect()


def initiate_request():
    global request_msg, student_index, property_editing, new_property_val, new_major, new_grade, new_fname, new_lname

    editing_codes = ["edit1", "edit2", "create1", "create2", "create3", "create4"]

    if request_msg not in editing_codes:
        request_msg = message_txt.get().casefold()
        message_txt.set("")

    if request_msg[0:12] == "show student":
        student_number = request_msg[13:]  # FIX THIS to account for extra spaces
        url = 'http://localhost:8080/getstudent'
        params = {'id': student_number}
        try:
            response = requests.get(url, params)
            response = response.content.decode()
            print(response)
            student = json.loads(response)
        except OSError:
            update_listbox("Error connecting to the server")
        else:
            try:
                print(student)
                if student["major"] is not None:
                    update_listbox(student_number + ". " + student["firstname"] + " " + student["lastname"] +
                                   " is a college student in grade " + student["grade"] + ",")
                    update_listbox("majoring in " + student["major"] + ". Created " + student["timecreated"] + ".")
                else:
                    update_listbox(student_number + ". " + student["firstname"] + " " + student["lastname"] +
                                   " is in grade " + student["grade"] + ". Created " + student["timecreated"])
            except KeyError:
                update_listbox("That student does not exist")

    elif request_msg == "show all students":
        message_txt.set("")
        url = 'http://localhost:8080/getstudent'
        params = {"id": "all"}
        try:
            response = requests.get(url, params)
            response = response.content.decode()
            response = json.loads(response)
            for key in response:
                student = response[key]
                if student["major"] is not None:
                    update_listbox(
                        key + ". " + student["firstname"] + " " + student["lastname"] + " is a college student in grade "
                        + student["grade"] + ",")
                    update_listbox("majoring in " + student["major"] + ". Created " + student["timecreated"] + ".")
                else:
                    update_listbox(key + ". " + student["firstname"] + " " + student["lastname"] + " is in grade "
                                   + student["grade"] + ". Created " + student["timecreated"])
        except OSError:
            if OSError:
                update_listbox("Error connecting to the server")
            else:
                update_listbox("Unknown error")

    elif request_msg[0:12] == "edit student":
        student_index = request_msg[13:]
        request_msg = "edit1"
        update_listbox("What would you like to change? choose firstname,")
        update_listbox("lastname, grade, or major")
    elif request_msg == "edit1":
        property_editing = message_txt.get()
        message_txt.set("")
        if property_editing == "firstname" or property_editing == "lastname" or property_editing == "grade" or property_editing == "major":
            update_listbox("What would you like to change the student's " + property_editing + " to?")
            request_msg = "edit2"
        else:
            request_msg = ""
            property_editing = ""
            student_index = ""
            update_listbox("That is not a student property. Edit cancelled.")
    elif request_msg == "edit2":
        print("edit2")
        new_property_val = message_txt.get()
        message_txt.set("")
        if new_property_val != "":
            url = 'http://localhost:8080/editstudent'
            print(student_index, property_editing, new_property_val)
            data = {"id": student_index, "attributeChange": property_editing, "attributeVal": new_property_val}
            response = None
            try:
                response = requests.post(url, data)
            except OSError:
                update_listbox("Error connecting to server")
            if response.status_code != 200:
                update_listbox("Student " + student_index + "'s " + property_editing + " has been edited")
            else:
                update_listbox("Error editing student")
        reset_modifications()
    elif request_msg[0:14] == "create student":
        update_listbox("What is the name of this new student?")
        request_msg = "create1"
    elif request_msg == "create1":
        new_fname = message_txt.get()
        message_txt.set("")
        if new_fname != "":
            new_fname = new_fname.capitalize()
            update_listbox("What is the student's last name?")
            request_msg = "create2"
        else:
            reset_modifications()
            update_listbox("First name value cannot be empty. Creation cancelled.")
    elif request_msg == "create2":
        new_lname = message_txt.get()
        message_txt.set("")
        if new_lname != "":
            new_lname = new_lname.capitalize()
            update_listbox("What grade is this student in?")
            request_msg = "create3"
        else:
            reset_modifications()
            update_listbox("Last name value cannot be empty. Creation cancelled.")
    elif request_msg == "create3":
        new_grade = message_txt.get()
        message_txt.set("")
        if new_grade != "":
            try:
                grade = int(new_grade)
                if grade > 14:
                    request_msg = ""
                    update_listbox("What is this student's major?")
                    request_msg = "create4"
                else:
                    # ERROR when editing a student. can do non-numerical grades.
                    url = 'http://localhost:8080/createstudent'
                    data = {"fname": new_fname, "lname": new_lname, "grade": new_grade}
                    response = None
                    try:
                        response = requests.post(url, data)
                    except OSError:
                        update_listbox("Error connecting to server")
                    if response.status_code == 200:
                        update_listbox("The student has been created.")
                    else:
                        update_listbox("Error creating student")
                    reset_modifications()
            except:
                print(Exception)
                update_listbox("Grade must be numerical")
                reset_modifications()
    elif request_msg == "create4":
        new_major = message_txt.get()
        message_txt.set("")
        if len(new_major) >- 1 and len(new_major) <=4:
            url = 'http://localhost:8080/createstudent'
            data = {"fname": new_fname, "lname": new_lname, "major": new_major, "grade": new_grade}
            response = None
            try:
                response = requests.post(url, data)
            except OSError:
                update_listbox("Error connecting to server")
            if response.status_code == 200:
                update_listbox("The student has been created.")
            else:
                update_listbox("Error creating student")
        else:
            update_listbox("Major must be between 1 and 4 characters. Creation cancelled.")
        reset_modifications()


def reset_modifications():
    """Cancels the edit or create action by setting the request_msg and all other attributes to empty strings"""
    global request_msg, new_lname, new_major, new_grade, property_editing, new_property_val, student_index, new_fname
    request_msg = ""
    property_editing = ""
    new_property_val = ""
    student_index = ""
    new_fname = ""
    new_lname = ""
    new_grade = ""
    new_major = ""


def update_listbox(msg):
    message_listbox.delete(0, len(messages))
    messages.append(msg)
    count = 0
    for message in messages:
        message_listbox.insert(count, message)
        count += 1
        message_listbox.yview_scroll(count, UNITS)


def connect():
    """Connects the client to the server and changes the GUI"""
    message_listbox.delete(0, len(messages))
    win.geometry("330x490")
    connect_button['text'] = 'Disconnect'
    connect_button['bg'] = 'light blue'
    message_listbox.grid(row=3, column=0, columnspan=2, ipady=120, sticky=N + S + E + W)


win = Tk()
win.geometry("330x51")
win.title("Client")

message_txt = StringVar()
scrname_entry_txt = StringVar()

client_id_label = Label(win, text="Client ID")
client_id_label.grid(row=1, column=0, padx=(0, 25), sticky=W)
client_id_entry = Entry(win, textvariable=scrname_entry_txt, justify=LEFT, width=35)
client_id_entry.grid(row=1, column=1, sticky=E)
client_id_entry.bind('<Key>', client_id_entry_handler)

connect_button = Button(text="Connect", width=45, command=connect)
connect_button.grid(row=2, column=0, columnspan=2)

scrollbar = Scrollbar(win)
message_listbox = Listbox(win, borderwidth=5, highlightcolor='light blue', yscrollcommand=scrollbar.set)
scrollbar.config(command=message_listbox.yview)

message_entry = Entry(win, textvariable=message_txt)
message_entry.grid(row=4, column=0, columnspan=2, ipadx=80, sticky=W)
message_entry.bind('<Key>', message_entry_event_handler)

send_btn = Button(win, text="Send", command=initiate_request)
send_btn.grid(row=4, column=1, ipadx=15, sticky=E)

win.mainloop()
