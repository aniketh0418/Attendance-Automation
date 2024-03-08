import tkinter as tk
from tkinter import filedialog
from twilio.rest import Client

# Function to take attendance and send messages
def take_attendance():
    n = int(entry_students.get())
    absentees_file = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[("Text files", "*.txt")])
    absentees = []
    presentees = []

    # Taking attendance
    for i in range(1, n + 1):
        roll_number = i
        present_status = entry_attendance[i].get().upper()
        if present_status == 'A':
            absentees.append(str(roll_number))
            presentees.append(f"Roll No. {roll_number} is absent.")
        elif present_status == '':
            absentees.append(str(roll_number))
            presentees.append(f"Roll No. {roll_number} is absent.")

    # Writing absentees to a file
    with open(absentees_file, 'w') as f:
        f.write("Today's Absentees:\n")
        f.write("\n".join(absentees))

    # Sending messages using Twilio
    # Your Twilio credentials go here
    account_sid = '' #add your twilio account sid here
    auth_token = '' #add your twilio account token here

    client = Client(account_sid, auth_token)

    # List of student contacts
    student_contacts = {
        '1': 'whatsapp:+91',  # add the actual phone numbers of students
        '2': 'whatsapp:+91',
        # Add more student contacts as needed
    }

    # Reading the absentees roll number from the text file
    with open(absentees_file, 'r') as f:
        absentees = [line.strip() for line in f]

    # Sending alert message to each absentee
    for roll_number in absentees:
        if roll_number in student_contacts:
            phone_number = student_contacts[roll_number]
            message = client.messages.create(
                body='Dear student, you were absent on today\'s class. Please contact your CR for further information.',
                from_='whatsapp:+14155238886',  
                to=phone_number,
            )

    # Sending message to teacher
    if absentees:
        teacher_contact = 'whatsapp:+91'  # add with the teacher's phone number
        message_to_teacher = "\n".join(absentees)
        message = client.messages.create(
            body=f"Today's Attendance Report:\n{message_to_teacher}",
            from_='+14155238886',  
            to=teacher_contact,
        )

    # Show alert message
    alert_label.config(text="Absentees were sent!")

# GUI Setup
root = tk.Tk()
root.title("Attendance Automation")

# Main Frame
main_frame = tk.Frame(root, padx=10, pady=10)
main_frame.pack(fill='both', expand=True)

# Label and entry for the number of students
label_students = tk.Label(main_frame, text="Enter the total number of students:")
label_students.pack()
entry_students = tk.Entry(main_frame)
entry_students.pack()

# Label for attendance status
label_attendance = tk.Label(main_frame, text="Enter 'A' for absent and 'P' for present:")
label_attendance.pack()

# Scrollable Frame for Entry Boxes
roll_frame = tk.Frame(main_frame)
roll_frame.pack(fill='both', expand=True)
canvas = tk.Canvas(roll_frame, height=200, width=200)
scrollbar = tk.Scrollbar(roll_frame, orient='vertical', command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox('all')
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side='left', fill='both', expand=True)
scrollbar.pack(side='right', fill='y')

# Entry boxes for attendance status
entry_attendance = {}

def create_attendance_entries():
    n = int(entry_students.get())
    rows = (n + 1) // 2
    cols = 6
    for i in range(1, n + 1):
        label = tk.Label(scrollable_frame, text=f"Roll No. {i}: ")
        label.grid(row=(i - 1) // cols, column=(i - 1) % cols * 3, padx=5, pady=5, sticky=tk.W)
        entry_attendance[i] = tk.Entry(scrollable_frame)
        entry_attendance[i].grid(row=(i - 1) // cols, column=(i - 1) % cols * 3 + 1, padx=5, pady=5, sticky=tk.W + tk.E)
        entry_attendance[i].bind("<Return>", move_to_next_entry)

def move_to_next_entry(event):
    current_roll = int(event.widget.get())
    next_roll = current_roll + 1
    if next_roll in entry_attendance:
        entry_attendance[next_roll].focus()

# Button to create attendance entries dynamically
create_entries_button = tk.Button(main_frame, text="Create Attendance Entries", command=create_attendance_entries)
create_entries_button.pack()

# Button to take attendance and send messages
attendance_button = tk.Button(main_frame, text="Take Attendance and Send Messages", command=take_attendance)
attendance_button.pack()

# Label for alert message
alert_label = tk.Label(main_frame, text="")
alert_label.pack()

root.mainloop()
