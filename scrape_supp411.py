#!/usr/bin/env python

"""
Author: harringr
Date: 201605010
Description: Python script to get data from supplements411
  http://www.supplement411.org/hrl/
  Supplement411 is published by USADA with list of risks for a number of nutritional supplements
  Supplement411 is governed by terms & conditions, including 'users may not reprint or distribute'
  This script and database is for extracting the data for purposes of analysis and use 
  in a proof-of-concept prototype as part of the whatsupp hack project
Licence: MIT License, 2016, see LICENSE.txt
"""

import lxml.html as lh
import MySQLdb as mdb
import yaml

from pprint import pprint
from selenium import webdriver
from selenium.webdriver.support.ui import Select


# Initialise mysql connection from own config file
# Example config file is given in config_example.yaml
with open('config.yaml', 'r') as f:
    config = yaml.load(f)


# Define connection
con = mdb.connect(config['hostname'], 
                  config['username'], 
                  config['password'], 
                  config['database']
                  )


"""Get data from Supplements411 page
Requires to go through registration / page (though currently no login accounts)
Use Selenium webdriver to go through process to load full page then get/return contents
"""
def get_supp411_page():
    
    browser = webdriver.Firefox()
    browser.get('http://www.supplement411.org/hrl/')

    firstname = browser.find_element_by_id("textfield-1010-inputEl")
    firstname.send_keys(config['supp411_firstname'])
    surname = browser.find_element_by_id("textfield-1011-inputEl")
    surname.send_keys(config['supp411_lastname'])

    email = browser.find_element_by_id("textfield-1012-inputEl")
    email.send_keys(config['supp411_email'])

    """ 
    Selecting the role from the 'dropdown' is a bit tricky 
     - it's not a 'select' element, which would use 'Select' class / methods
     - instead it's a unordered list generated by clicking on the combobox (by JS?)
    """

    # Click on combobox to display list of divs items
    browser.find_element_by_id("combobox-1013-inputEl").click()

    # Select specific element 'Other' - use css selector
    css_selector = get_css_selector_from_role(config['supp411_role'])

    browser.find_element_by_css_selector(css_selector).click()

    # Click on checkbox
    browser.find_element_by_id("checkbox-1015-inputEl").click()

    # Click submit button 
    browser.find_element_by_id("button-1016").click()

    """After registration details have been supplied and entered
    Page reloads with credentials -> get new page contents into variable"""
    page_contents = browser.page_source

    # Finished getting page contents so can quit browser
    browser.quit()
    
    return page_contents


def get_css_selector_from_role(role):
    
    selectors = {
        'Athlete': '#boundlist-1029-listEl > ul > li:nth-child(1)',
        'Coach': '#boundlist-1029-listEl > ul > li:nth-child(2)',
        'Agent': '#boundlist-1029-listEl > ul > li:nth-child(3)',
        'Medical professional': '#boundlist-1029-listEl > ul > li:nth-child(4)',
        'Parent': '#boundlist-1029-listEl > ul > li:nth-child(5)',
        'Sport administrator': '#boundlist-1029-listEl > ul > li:nth-child(6)',
        'Other': '#boundlist-1029-listEl > ul > li:nth-child(7)',
    }

    return selectors[role]


"""
"""
def parse_supp411(page_contents):
    
    # Get html tree from webpage content, using lxml.html
    tree = lh.fromstring(page_contents)
    print tree

    # Get products table from 
    table = tree.cssselect("#gridview-1027-table")[0]
    trs = table.cssselect("tr")
    
    for tr in trs:

        tds = tr.cssselect("td")

        data = dict()
        data['name'] = tds[0].getchildren()[0].getchildren()[0].text
        data['company'] = tds[1].getchildren()[0].getchildren()[0].text
        data['label'] = tds[2].getchildren()[0].getchildren()[0].text
        data['classification'] = tds[3].getchildren()[0].getchildren()[0].text
        data['updated'] = tds[4].getchildren()[0].getchildren()[0].text
        data['comments'] = tds[5].getchildren()[0].getchildren()[0].text

        pprint(data)
        product_data_to_db(data)


""" Insert data into mysql table """
def product_data_to_db(data):

    with con:

        cur = con.cursor()
        sql = """INSERT INTO supplement411 (name, company, label, classification, updated, comments) 
                 VALUES (%s, %s, %s, %s, %s, %s)"""
        cur.execute(sql, (data['name'], 
                          data['company'], 
                          data['label'], 
                          data['classification'],
                          data['updated'],
                          data['comments'],
                          ))


def main():

    page_contents = get_supp411_page()
    parse_supp411(page_contents)

if __name__ == '__main__':
    main()
