# -*- coding: utf-8 -*-
# https://www.pythontutorial.net/tkinter/
# https://de.wikipedia.org/wiki/VCard
# app/ui.py

"""This module provides a user interface."""
import tkinter as tk
from tkinter import Frame
from tkinter import LabelFrame
from tkinter import ttk
from tkinter import messagebox
from tkinter import PhotoImage
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import asksaveasfile

from .data import inital_data_struct
from .data import print_dict

from .db import read_db_table
from .db import read_single_db_table_enty
from .db import search_db_table
from .db import delete_db_entry
from .db import add_db_entry
from .db import update_db_entry

from .vcard import vcard_string_generator
from .vcard import txt2filename

from .qr import qr_vcard_generator

def update_table(table, rows):
    table.delete(*table.get_children()) # keep table empty
    for row in rows:
      # print(row)
      table.insert("", "end", values=row)
    return

class Window(Frame):
  def __init__(self, master = None):
    Frame.__init__(self,master)
    
    self.master = master
    self.init_window()
    self.QrWindow = None
     
  def init_window(self):
   
    self.master.title("VCARD App")
    self.pack(fill=tk.BOTH, expand=1)

    ###vcard = inital_data_struct()
    ##print_dict(vcard)     
    
    # Sizegrip
    sizegrip = ttk.Sizegrip(self.master)
    sizegrip.pack(fill="both", expand="yes", padx=5, pady=5)
    
    # Menu:
    menu = tk.Menu(self.master)
    self.master.config(menu=menu)
    
    file = tk.Menu(menu, tearoff=0)
    file.add_command(label='Exit', command = self.client_exit)
    file.add_command(label='Save VCARD', command = self.save_vcard_file)
    
    menu.add_cascade(label='File', menu=file)
    
    # Frames:  
    self.wrapper1 = LabelFrame(self, text="VCARD List")
    self.wrapper2 = LabelFrame(self, text="VCARD Search")
    self.wrapper3 = LabelFrame(self, text="VCARD Data")
    self.wrapper4 = LabelFrame(self, text="VCARD Status")


    # Window Scrollbar:

    self.master_scroll_y = ttk.Scrollbar(self, orient='vertical')

    # Wrapper Frames
    #self.wrapper2.pack(fill="both", expand="yes", padx=5, pady=5)
    #self.wrapper1.pack(fill="both", expand="yes", padx=5, pady=5)
    #self.wrapper3.pack(fill="both", expand="yes", padx=5, pady=5)
    #self.wrapper3_scroll_y.pack(side="right", fill="y")
    #self.wrapper4.pack(fill="both", expand="yes", padx=5, pady=5)

    self.wrapper2.grid(row=0, column=0, padx=5, pady=5, sticky=tk.EW)
    self.wrapper1.grid(row=1, column=0, padx=5, pady=5, sticky=tk.EW)
    self.wrapper3.grid(row=2, column=0, padx=5, pady=5, sticky=tk.EW)
    self.wrapper4.grid(row=3, column=0, padx=5, pady=5, sticky=tk.EW)
    self.master_scroll_y.grid(row=0, column=1, padx=0, pady=0, rowspan=4, sticky=tk.NS)
    
   
    # Table:
    # https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview
    # https://stackoverflow.com/questions/63973865/tkinter-treeview-resizing-the-treeview-to-fit-screen
    # https://discuss.dizzycoding.com/tk-treeview-column-sort/
    # https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/ttk-Treeview.html
    
    self.table = ttk.Treeview(self.wrapper1, columns=(1,2,3,4,5,6,7,8), show="headings", height="8")

    self.table.heading(1, text="ID", command=lambda: self.table_heading_clk("ID"), anchor=tk.W)
    self.table.heading(2, text="First Name", command=lambda: self.table_heading_clk("N_FIRST"), anchor=tk.W)
    self.table.heading(3, text="Last Name", command=lambda: self.table_heading_clk("N_LAST"), anchor=tk.W)
    self.table.heading(4, text="Company", command=lambda: self.table_heading_clk("ORG"), anchor=tk.W)
    self.table.heading(5, text="E-Mail", command=lambda: self.table_heading_clk("EMAIL"), anchor=tk.W)
    self.table.heading(6, text="Title", command=lambda: self.table_heading_clk("TITLE"), anchor=tk.W)
    self.table.heading(7, text="Role", command=lambda: self.table_heading_clk("ROLE"), anchor=tk.W)
    self.table.heading(8, text="Category", command=lambda: self.table_heading_clk("CATEGORIES"), anchor=tk.W)

    self.table.column(1, minwidth=25, stretch=True, width=30)
    self.table.column(2, minwidth=25, stretch=True, width=100)
    self.table.column(3, minwidth=25, stretch=True, width=100)
    self.table.column(4, minwidth=25, stretch=True, width=100)
    self.table.column(5, minwidth=25, stretch=True, width=150)
    self.table.column(6, minwidth=25, stretch=True, width=120)
    self.table.column(7, minwidth=25, stretch=True, width=120)
    self.table.column(8, minwidth=25, stretch=True, width=120)
  
    # Scrollbar Wrapper 1:
    # https://www.pythontutorial.net/tkinter/tkinter-scrollbar/
    self.table_scroll_x = ttk.Scrollbar(self.wrapper1, orient='horizontal')
    self.table_scroll_x.configure(command=self.table.xview)
    self.table.configure(xscrollcommand=self.table_scroll_x.set)
    
    self.table_scroll_y = ttk.Scrollbar(self.wrapper1, orient='vertical')
    self.table_scroll_y.configure(command=self.table.yview)
    self.table.configure(yscrollcommand=self.table_scroll_y.set)

    self.table.grid(row=0, column=0, padx=0, pady=0, sticky=tk.EW)
    self.table_scroll_x.grid(row=1, column=0, padx=0, pady=0, sticky=tk.EW)
    self.table_scroll_y.grid(row=0, column=1, padx=0, pady=0, sticky=tk.NS)
 
    
    # Action on double click row
    self.table.bind('<Double 1>', self.get_row_data) 
    
     # Read data to table
    self.table.order = "N_LAST" # Define the order more globaly
    
    rows = read_db_table(self.table.order)
    update_table(self.table, rows)

    # Search Section
    self.search_lbl = tk.Label(self.wrapper2, text="Search")
    self.search_lbl.grid(row=0, column=0, padx=5, pady=3)
    self.search_ent = tk.Entry(self.wrapper2) ###, textvariable=search_query)
    self.search_ent.grid(row=0, column=1, padx=5, pady=3)
    self.search_ent.bind('<Return>', self.search_enter)
    self.search_btn = tk.Button(self.wrapper2, text="Search", command=self.search_clk)
    self.search_btn.grid(row=0, column=2, padx=5, pady=3)
    self.clear_search_btn = tk.Button(self.wrapper2, text="Clear", command=self.clear_clk)
    self.clear_search_btn.grid(row=0, column=3, padx=5, pady=3)

    # User Data Section

    # Row 0
    self.id_lbl = tk.Label(self.wrapper3, text="ID")
    self.id_lbl.grid(row=0, column=0, padx=5, pady=3, sticky=tk.E)
    self.id_ent = tk.Entry(self.wrapper3)
    self.id_ent.grid(row=0, column=1, padx=5, pady=3)
    self.id_ent.config(state='disabled')

    self.notes_lbl = tk.Label(self.wrapper3, text="Notes")
    self.notes_lbl.grid(row=0, column=3, padx=5, pady=3, sticky=tk.E)
    self.notes_ent = ScrolledText(self.wrapper3, width=35, height=10)
    self.notes_ent.grid(row=0, column=4, padx=5, pady=3, rowspan=6, columnspan=2)

    # Row 1
    self.f_name_lbl = tk.Label(self.wrapper3, text="First Name")
    self.f_name_lbl.grid(row=1, column=0, padx=5, pady=3, sticky=tk.E)
    self.f_name_ent = tk.Entry(self.wrapper3)
    self.f_name_ent.grid(row=1, column=1, padx=5, pady=3)
    
    self.l_name_lbl = tk.Label(self.wrapper3, text="Last Name")
    self.l_name_lbl.grid(row=1, column=2, padx=5, pady=3, sticky=tk.E)
    self.l_name_ent = tk.Entry(self.wrapper3)
    self.l_name_ent.grid(row=1, column=3, padx=5, pady=3)

     # Row 2
    self.company_lbl = tk.Label(self.wrapper3, text="Company")
    self.company_lbl.grid(row=2, column=0, padx=5, pady=3, sticky=tk.E)
    self.company_ent = tk.Entry(self.wrapper3)
    self.company_ent.grid(row=2, column=1, padx=5, pady=3)

    self.title_lbl = tk.Label(self.wrapper3, text="Title")
    self.title_lbl.grid(row=2, column=2, padx=5, pady=3, sticky=tk.E)
    self.title_ent = tk.Entry(self.wrapper3)
    self.title_ent.grid(row=2, column=3, padx=5, pady=3)

    # Row 3    

    self.role_lbl = tk.Label(self.wrapper3, text="Role")
    self.role_lbl.grid(row=3, column=2, padx=5, pady=3, sticky=tk.E)
    self.role_ent = tk.Entry(self.wrapper3)
    self.role_ent.grid(row=3, column=3, padx=5, pady=3)
    
    # Row 4    
    self.email_lbl = tk.Label(self.wrapper3, text="E-Mail")
    self.email_lbl.grid(row=4, column=0, padx=5, pady=3, sticky=tk.E)
    self.email_ent = tk.Entry(self.wrapper3)
    self.email_ent.grid(row=4, column=1, padx=5, pady=3)

    self.url_lbl = tk.Label(self.wrapper3, text="URL")
    self.url_lbl.grid(row=4, column=2, padx=5, pady=3, sticky=tk.E)
    self.url_ent = tk.Entry(self.wrapper3)
    self.url_ent.grid(row=4, column=3, padx=5, pady=3)

    #Row 5
    self.phone_w_lbl = tk.Label(self.wrapper3, text="Phone (Work)")
    self.phone_w_lbl.grid(row=5, column=0, padx=5, pady=3, sticky=tk.E)
    self.phone_w_ent = tk.Entry(self.wrapper3)
    self.phone_w_ent.grid(row=5, column=1, padx=5, pady=3)

    self.cell_w_lbl = tk.Label(self.wrapper3, text="Cell (Work)")
    self.cell_w_lbl.grid(row=5, column=2, padx=5, pady=3, sticky=tk.E)
    self.cell_w_ent = tk.Entry(self.wrapper3)
    self.cell_w_ent.grid(row=5, column=3, padx=5, pady=3)

    # Row 6
    self.phone_h_lbl = tk.Label(self.wrapper3, text="Phone (Home)")
    self.phone_h_lbl.grid(row=6, column=0, padx=5, pady=3, sticky=tk.E)
    self.phone_h_ent = tk.Entry(self.wrapper3)
    self.phone_h_ent.grid(row=6, column=1, padx=5, pady=3)

    self.cell_h_lbl_h_lbl = tk.Label(self.wrapper3, text="Cell (Home)")
    self.cell_h_lbl_h_lbl.grid(row=6, column=2, padx=5, pady=3, sticky=tk.E)
    self.cell_h_ent = tk.Entry(self.wrapper3)
    self.cell_h_ent.grid(row=6, column=3, padx=5, pady=3)
    
    self.categories_lbl = tk.Label(self.wrapper3, text="Category")
    self.categories_lbl.grid(row=6, column=4, padx=5, pady=3, sticky=tk.E)
    self.categories_ent = tk.Entry(self.wrapper3)
    self.categories_ent.grid(row=6, column=5, padx=5, pady=3)

    #self.wrapper3_scroll_y = ttk.Scrollbar(self.wrapper3, orient='vertical')
    #self.wrapper3_scroll_y.grid(row=0, column=5, padx=0, pady=0, rowspan=4)

   
    # https://www.pythontutorial.net/tkinter/tkinter-grid/

    # Row 7: Buttons:
    self.clear_data_btn = tk.Button(self.wrapper3, text="Clear", command=self.clear_data_text_boxes)
    self.clear_data_btn.grid(row=7, column=0, padx=5, pady=3)   
    self.add_btn = tk.Button(self.wrapper3, text="Add", command=self.add_user_clk)
    self.add_btn.grid(row=7, column=1, padx=5, pady=3)
    self.update_btn = tk.Button(self.wrapper3, text="Update", command=self.update_user_clk)
    self.update_btn.grid(row=7, column=2, padx=5, pady=3)
    self.delete_btn = tk.Button(self.wrapper3, text="Delete", command=self.delete_user_clk)
    self.delete_btn.grid(row=7, column=3, padx=5, pady=3)
    self.qr_btn = tk.Button(self.wrapper3, text="Create QR", command=self.qr_create_clk)
    self.qr_btn.grid(row=7, column=4, padx=5, pady=3)   

    # Status Bar:
    self.status_lbl = tk.Label(self.wrapper4, text="App started")
    self.status_lbl.grid(row=0, column=0, padx=5, pady=3, sticky=tk.W)



  ######################################################
    
  def update_status(self, message):
    #self.status_lbl.set('end', 'Status: ' + message) # Insert entry
    self.status_lbl.config(text='Status: ' + message)
    return
    
  # Get data set to edit
  def get_row_data(self, event):
    #rowid = self.table.identify_row(event.y)
    item = self.table.item(self.table.focus())
    #print(item['values'][0], rowid)

    # Get data from database:
    id = item['values'][0]
    row = read_single_db_table_enty(id)
    #print("Get Row Data:")
    #print(row[0])
    #print(row[0][0])
    #self.update_status("test")
  
    # Clear Text Fields:
    self.clear_data_text_boxes()
    # Fill Text Fields:
    self.id_ent.config(state='normal')
    self.id_ent.insert('end', row[0][0]) # Insert entry 
    self.id_ent.config(state='disabled')
    
    self.f_name_ent.insert('end', row[0][1]) # Insert entry 
    self.l_name_ent.insert('end', row[0][2]) # Insert entry 
    self.company_ent.insert('end', row[0][3]) # Insert entry 
    self.email_ent.insert('end', row[0][4]) # Insert entry 
    self.url_ent.insert('end', row[0][5]) # Insert entry 
    self.cell_w_ent.insert('end', row[0][6]) # Insert entry 
    self.phone_w_ent.insert('end', row[0][7]) # Insert entry 
    self.cell_h_ent.insert('end', row[0][8]) # Insert entry 
    self.phone_h_ent.insert('end', row[0][9]) # Insert entry 
    self.title_ent.insert('end', row[0][10]) # Insert entry 
    self.role_ent.insert('end', row[0][11]) # Insert entry 
    self.categories_ent.insert('end', row[0][12]) # Insert entry
    self.notes_ent.insert('end', row[0][13]) # Insert entry 

    return
    
  def clear_data_text_boxes(self):   
    # Make Text Fields Empty    
    self.id_ent.config(state='normal')
    self.id_ent.delete(0,'end') # Delete entry 
    self.id_ent.config(state='disabled')
    
    self.f_name_ent.delete(0,'end') # Delete entry
    self.l_name_ent.delete(0,'end') # Delete entry
    self.company_ent.delete(0,'end') # Delete entry
    self.email_ent.delete(0,'end') # Delete entry
    self.url_ent.delete(0,'end') # Delete entry
    self.cell_w_ent.delete(0,'end') # Delete entry
    self.phone_w_ent.delete(0,'end') # Delete entry
    self.cell_h_ent.delete(0,'end') # Delete entry
    self.phone_h_ent.delete(0,'end') # Delete entry
    self.title_ent.delete(0,'end') # Delete entry
    self.role_ent.delete(0,'end') # Delete entry
    self.categories_ent.delete(0,'end') # Delete entry

    self.notes_ent.delete(1.0,'end') # Delete entry
    
    return

  # Table heading click event.
  def table_heading_clk(self, column_sql):
    if column_sql == self.table.order:
      self.table.order = column_sql + " DESC"
    else:
      self.table.order = column_sql
    rows = read_db_table(self.table.order)
    update_table(self.table, rows)
    #messagebox.showinfo("Info",f"You have clicked: {column_sql}.")
    return
  
  def clear_clk(self):
    # Read data to table
    rows = read_db_table(self.table.order)
    update_table(self.table, rows)
    self.search_ent.delete(0,'end') # Empty search entry box 
    return
    
  def search_enter(self, event):
    # When Enter was clicked
    # Enter Event needs secound argument
    # print(f"Search Event: {event}")
    self.search_clk()
    return
    
  def search_clk(self):
    search_query = self.search_ent.get()
    # Read data to table
    if search_query == "": 
        rows = read_db_table(self.table.order)
    else:
        rows = search_db_table(search_query)
    update_table(self.table, rows)
    return
    
  def add_user_clk(self):
    f_name = self.f_name_ent.get()
    l_name = self.l_name_ent.get()
    company = self.company_ent.get()
    email = self.email_ent.get()
    url = self.url_ent.get()
    cell_w = self.cell_w_ent.get()
    phone_w = self.phone_w_ent.get()
    cell_h = self.cell_h_ent.get()
    phone_h = self.phone_h_ent.get()
    title = self.title_ent.get()
    role = self.role_ent.get()
    categories = self.categories_ent.get()
    notes = self.notes_ent.get('1.0', 'end-1c')
    
    if(f_name and not f_name.isspace()): # only execute when name field is filled
      add_db_entry(f_name, l_name, company, email, url, cell_w, phone_w, cell_h, phone_h, title, role, categories, notes)
      self.clear_clk()
      self.clear_data_text_boxes()
    else:
      messagebox.showinfo("Add","To create new entry:\nFirst name should not be empty.")
    return

  def update_user_clk(self):
    id = self.id_ent.get()
    f_name = self.f_name_ent.get()
    l_name = self.l_name_ent.get()
    company = self.company_ent.get()
    email = self.email_ent.get()
    url = self.url_ent.get()
    cell_w = self.cell_w_ent.get()
    phone_w = self.phone_w_ent.get()
    cell_h = self.cell_h_ent.get()
    phone_h = self.phone_h_ent.get()
    title = self.title_ent.get()
    role = self.role_ent.get()
    categories = self.categories_ent.get()
    notes = self.notes_ent.get('1.0', 'end-1c')
    
    if messagebox.askyesno("Confirm update?", f"Are you sure you want to update this ID: {id}?"):
        
        update_db_entry(id, f_name, l_name, company, email, url, cell_w, phone_w, cell_h, phone_h, title, role, categories, notes)
        self.clear_clk()
        self.clear_data_text_boxes()
    return

  def delete_user_clk(self):
    id = self.id_ent.get()
    if (id):
      if messagebox.askyesno("Confirm delete?", f"Are you sure you want to delete this ID: {id}?"):
        delete_db_entry(id)
        self.clear_clk()
        self.clear_data_text_boxes()
    return

  # Create QR Window View
  def qr_create_clk(self):
    #id = self.id_ent.get()
    f_name = self.f_name_ent.get()
    l_name = self.l_name_ent.get()
    company = self.company_ent.get()
    email = self.email_ent.get()
    url = self.url_ent.get()
    cell_w = self.cell_w_ent.get()
    phone_w = self.phone_w_ent.get()
    cell_h = self.cell_h_ent.get()
    phone_h = self.phone_h_ent.get()
    title = self.title_ent.get()
    role = self.role_ent.get()
    categories = self.categories_ent.get()
    notes = self.notes_ent.get('1.0', 'end-1c')
    
    # only execute when name field is filled
    if(f_name and not f_name.isspace()):
      
      img = qr_vcard_generator(f_name, l_name, company, email, url, cell_w, phone_w, cell_h, phone_h, title, role, categories, notes)
      #img = PhotoImage(file='qr.png')
      
      # Create QR Window
      #if self.QrWindow == None or not tk.Toplevel.winfo_exists(self.QrWindow):
      self.QrWindow = tk.Toplevel()
      self.QrWindow.title("VCARD QR Code") 
      self.QrWindow.iconphoto(False, tk.PhotoImage(file='./app/icon.png'))
      
      self.qr_image = tk.PhotoImage(file='./app/qr.png')
      self.qr_image_btn = tk.Button(self.QrWindow, image=self.qr_image, borderwidth=0, bd=0, highlightthickness=0, command = self.QrWindow.destroy).pack()
      self.qr_image_btn = self.qr_image # Importen to get correct view in Linux
            
      
    else:
      messagebox.showinfo("QR Code","To create QR code\nFirst name should not be empty.")
    return

  
  def save_vcard_file(self):
    #id = self.id_ent.get()
    f_name = self.f_name_ent.get()
    l_name = self.l_name_ent.get()
    company = self.company_ent.get()
    email = self.email_ent.get()
    url = self.url_ent.get()
    cell_w = self.cell_w_ent.get()
    phone_w = self.phone_w_ent.get()
    cell_h = self.cell_h_ent.get()
    phone_h = self.phone_h_ent.get()
    title = self.title_ent.get()
    role = self.role_ent.get()
    categories = self.categories_ent.get()
    notes = self.notes_ent.get('1.0', 'end-1c')
    
    # only execute when name field is filled
    if(f_name and not f_name.isspace()): 

      vcard_str = vcard_string_generator(f_name, l_name, company, email, url, cell_w, phone_w, cell_h, phone_h, title, role, categories, notes)
      
      #print("Save File")
      # Define inital File Name
      initial_filename = f_name
      if(l_name and not l_name.isspace()): initial_filename += ("_" + l_name)
      if(company and not company.isspace()): initial_filename += ("_" + company)
      initial_filename += '.vcf'
      
      vcard_file = asksaveasfile(initialfile = initial_filename, defaultextension=".vcf",filetypes=[("vCards","*.vcf"),("All Files","*.*")])
      if vcard_file is None:
        return
      vcard_file.write(vcard_str)
      vcard_file.close()
      #print("File saved as ", vcard_file)
      
    else:
        messagebox.showinfo("VCARD","To create VCARD File\nFirst name should not be empty.")
    return
    
  def client_exit(self):
    exit()

