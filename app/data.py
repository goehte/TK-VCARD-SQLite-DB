# -*- coding: utf-8 -*-
# app/data.py


def inital_data_struct():
  vcard_data_struct = {
     # [#value, #get_used, #in_table, #in_tab1]
    'ID': ['', True, True, True],
    'N_FIRST': ['', True, True, True],
    'N_LAST': ['', True, True, True],
    'N_ADD': ['', False, False, False],
    'N_PRE': ['', False, False, False],
    'N_SUF': ['', False, False, False],
    'NICKNAME': ['', False, False, False],
    'GENDER': ['', False, False, False],
    'ORG': ['', True, True, True],
    'ROLE': ['', False, False, False],
    'TITLE': ['', True, True, True],
    'EMAIL': ['', True, True, True],
    'URL': ['', False, False, False],
    'NOTE': ['', True, False, True],
    'ADR_HOME': ['', False, False, False],
    'ADR_WORK': ['', False, False, False],
    'TEL_WORK_CELL': ['', False, False, False],
    'TEL_WORK_VOICE': ['', True, True, True],
    'TEL_HOME_CELL': ['', False, False, False],
    'TEL_HOME_VOICE': ['', False, False, False],
    'CATEGORIES': ['', False, False, False],
    'BDAY': ['', False, False, False],
    'ANNIVERSARY': ['', False, False, False],
    'TZ': ['', False, False, False],
    'REV': ['', True, False, False]
  }
  return vcard_data_struct

def get_list_from_dict(dict):
    list = []
    for key in dict.keys():
        list.append(key)         
    return list

def print_dict(dict):
    for key in dict.keys():
      print(f"{key} : {dict[key][1]}") 