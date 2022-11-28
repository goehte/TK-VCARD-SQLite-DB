# -*- coding: utf-8 -*-
# https://www.youtube.com/watch?v=i4qLI9lmkqw
# 09.10.2022: Bis Minute 41 -nächster schritt user daten updaten
# app/main.py

"""This module provides main application."""

import tkinter as tk

from .ui import Window
     
def main():

  window = tk.Tk()
  window.title("App Title")
  window.geometry("900x600")
  window.iconphoto(False, tk.PhotoImage(file='./app/icon.png'))
  
  app = Window(window)
  window.mainloop()


