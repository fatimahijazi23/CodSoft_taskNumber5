import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

class ContactBook:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book")
        self.root.configure(bg="white")  

        self.contacts = {}
        self.loadContacts()

        self.frame = tk.Frame(root, padx=20, pady=20, bg="white")  
        self.frame.pack()

        self.fontStyle = ("Arial", 14)

        self.nameLabel = tk.Label(self.frame, text="Name:", font=self.fontStyle, bg="white")
        self.nameLabel.grid(row=0, column=0, padx=10, pady=5)  

        self.nameEntry = tk.Entry(self.frame, font=self.fontStyle)
        self.nameEntry.grid(row=0, column=1, padx=10, pady=5)  

        self.phoneLabel = tk.Label(self.frame, text="Phone:", font=self.fontStyle, bg="white")
        self.phoneLabel.grid(row=1, column=0, padx=10, pady=5)

        self.phoneEntry = tk.Entry(self.frame, font=self.fontStyle)
        self.phoneEntry.grid(row=1, column=1, padx=10, pady=5)

        self.emailLabel = tk.Label(self.frame, text="Email:", font=self.fontStyle, bg="white")
        self.emailLabel.grid(row=2, column=0, padx=10, pady=5)

        self.emailEntry = tk.Entry(self.frame, font=self.fontStyle)
        self.emailEntry.grid(row=2, column=1, padx=10, pady=5)

        self.addressLabel = tk.Label(self.frame, text="Address:", font=self.fontStyle, bg="white")
        self.addressLabel.grid(row=3, column=0, padx=10, pady=5)

        self.addressEntry = tk.Entry(self.frame, font=self.fontStyle)
        self.addressEntry.grid(row=3, column=1, padx=10, pady=5)

        self.addButton = tk.Button(self.frame, text="Add Contact", command=self.addContact, font=self.fontStyle, bg="pink")
        self.addButton.grid(row=4, column=0, columnspan=2, pady=10, sticky="we")  

        self.viewButton = tk.Button(self.frame, text="View Contacts", command=self.viewContacts, font=self.fontStyle, bg="pink")
        self.viewButton.grid(row=5, column=0, columnspan=2, pady=10, sticky="we")

        self.searchButton = tk.Button(self.frame, text="Search Contact", command=self.searchContact, font=self.fontStyle, bg="pink")
        self.searchButton.grid(row=6, column=0, columnspan=2, pady=10, sticky="we")

        self.updateButton = tk.Button(self.frame, text="Update Contact", command=self.updateContact, font=self.fontStyle, bg="pink")
        self.updateButton.grid(row=7, column=0, columnspan=2, pady=10, sticky="we")

        self.deleteButton = tk.Button(self.frame, text="Delete Contact", command=self.deleteContact, font=self.fontStyle, bg="pink")
        self.deleteButton.grid(row=8, column=0, columnspan=2, pady=10, sticky="we")

    def loadContacts(self):
        if os.path.exists("contacts.json"):
            with open("contacts.json", "r") as f:
                self.contacts = json.load(f)

    def saveContacts(self):
        with open("contacts.json", "w") as f:
            json.dump(self.contacts, f)

    def addContact(self):
        name = self.nameEntry.get()
        phone = self.phoneEntry.get()
        email = self.emailEntry.get()
        address = self.addressEntry.get()

        if name and phone:
            self.contacts[name] = {"phone": phone, "email": email, "address": address}
            self.saveContacts()
            messagebox.showinfo("Success", "Contact added successfully!")
        else:
            messagebox.showwarning("Input Error", "Name and Phone are required fields!")

    def viewContacts(self):
        contactList = "\n".join([f"{name}: {info['phone']}" for name, info in self.contacts.items()])
        if contactList:
            messagebox.showinfo("Contact List:", contactList)
        else:
            messagebox.showinfo("Contact List:", "No contacts found!")

    def searchContact(self):
        searchTerm = simpledialog.askstring("Search Contact", "Enter name or phone number:")
        if searchTerm:
            results = [f"{name}: {info['phone']}" for name, info in self.contacts.items() if searchTerm in name or searchTerm in info['phone']]
            if results:
                messagebox.showinfo("Search Results", "\n".join(results))
            else:
                messagebox.showinfo("Search Results", "No contacts found!")

    def updateContact(self):
        name = simpledialog.askstring("Update Contact", "Enter the name of the contact to update:")
        if name in self.contacts:
            currentInfo = self.contacts[name]
            currentPhone = currentInfo.get("phone", "")
            currentEmail = currentInfo.get("email", "")
            currentAddress = currentInfo.get("address", "")

            self.nameEntry.delete(0, tk.END)
            self.nameEntry.insert(0, name)
            self.phoneEntry.delete(0, tk.END)
            self.phoneEntry.insert(0, currentPhone)
            self.emailEntry.delete(0, tk.END)
            self.emailEntry.insert(0, currentEmail)
            self.addressEntry.delete(0, tk.END)
            self.addressEntry.insert(0, currentAddress)

            self.updateButton.config(command=lambda: self.saveUpdatedContact(name))
        else:
            messagebox.showwarning("Not Found", "Contact not found!")

    def saveUpdatedContact(self, name):
        phone = self.phoneEntry.get()
        email = self.emailEntry.get()
        address = self.addressEntry.get()

        self.contacts[name] = {"phone": phone, "email": email, "address": address}
        self.saveContacts()
        messagebox.showinfo("Success", "Contact updated successfully!")

    def deleteContact(self):
        name = simpledialog.askstring("Delete Contact", "Enter name of the contact to delete:")
        if name in self.contacts:
            del self.contacts[name]
            self.saveContacts()
            messagebox.showinfo("Success", "Contact deleted successfully!")
        else:
            messagebox.showwarning("Not Found", "Contact not found!")

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBook(root)
    root.mainloop()
