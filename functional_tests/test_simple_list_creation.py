from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from unittest import skip
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys
import unittest
import time
import os



class NewVisitorTest(FunctionalTest):


    def test_can_start_a_list_for_one_user(self):
        #edith has heard about a cool new online to-do app. Seh Dja
        #Edith heard about a cool new online to-do app.
        #she goes to check out its homepage
        self.browser.get(self.live_server_url)
        # self.browser.get('http://localhost:8000')

        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        inputbox.send_keys('Buy peacock feathers')
        # When she hits enter, the page updates, and now the page list/
        #"1: Buy peacock featers" as an item in a to-do list table
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        #There is still a text box inviting her to add another item.
        #She enters "Use peacock feathers to make a fly"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)


        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        #edith starts another to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        #she notices her list has a unique url
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        #we introduce francis, who comes along on the site

        #we use a new brother session for francis
        self.browser.quit()

        self.browser = webdriver.Firefox()

        #Francis visits the home page. There is no sign of Edith's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        #francis starts a new list by entering a new item.
        #he is less exotic than edith...
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        #francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        #Again, there is no trace of Edith's lists
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peackock feathers', page_text)
        self.assertIn('Buy milk',page_text)
