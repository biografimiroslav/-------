import sqlite3
import tkinter as tk
from tkinter import ttk


conn = sqlite3.connect("contacts.db")


cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT
    )
''')
conn.commit()


def add_contact():
    name = name_entry.get()
    email = email_entry.get()
    cursor.execute('INSERT INTO contacts (name, email) VALUES (?, ?)', (name, email))
    conn.commit()
    status_label.config(text="Контакт додано!")
    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)

# Функція для виведення всіх контактів
def list_contacts():
    cursor.execute('SELECT * FROM contacts')
    contacts = cursor.fetchall()
    if contacts:
        contact_list.delete(*contact_list.get_children())
        for contact in contacts:
            contact_list.insert("", "end", values=(contact[0], contact[1], contact[2]))
    else:
        status_label.config(text="Список контактів порожній")


root = tk.Tk()
root.title("Менеджер контактів")


frame = ttk.Frame(root)
frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

name_label = ttk.Label(frame, text="Ім'я:")
name_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
name_entry = ttk.Entry(frame)
name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

email_label = ttk.Label(frame, text="Email:")
email_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
email_entry = ttk.Entry(frame)
email_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

add_button = ttk.Button(frame, text="Додати контакт", command=add_contact)
add_button.grid(row=2, column=0, columnspan=2, pady=10)

list_button = ttk.Button(frame, text="Вивести список контактів", command=list_contacts)
list_button.grid(row=3, column=0, columnspan=2, pady=10)

status_label = ttk.Label(frame, text="", foreground="green")
status_label.grid(row=4, column=0, columnspan=2)

contact_list = ttk.Treeview(frame, columns=("ID", "Ім'я", "Email"), show="headings")
contact_list.heading("ID", text="ID")
contact_list.heading("Ім'я", text="Ім'я")
contact_list.heading("Email", text="Email")
contact_list.grid(row=5, column=0, columnspan=2, pady=10)
contact_list.column("ID", width=30)
contact_list.column("Ім'я", width=100)
contact_list.column("Email", width=150)


root.mainloop()


conn.close()
