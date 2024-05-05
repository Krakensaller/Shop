import logging
import os
import datetime
from dotenv import load_dotenv, find_dotenv

from tbselenium.tbdriver import TorBrowserDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from db import DB

load_dotenv(find_dotenv())

logging.basicConfig(filename="spider_log.txt", level=logging.ERROR)


class whiteHouseMarketSpider():
    """
    This spider extracts narcotic product information from the darknet marketplace 'The White House Market'
    Each product is extracted as a dictionary item and inserted into a postgres database
    
    The spider extracts the following information for each product:

    str website: the website that the product is listed on (WhiteHouseMarket for this spider)
    str vendor: the name of the product lister
    str title: the title description of the product listing
    str update_at: date that the product listing was extracted (GST)
    str category: broad category of the drug i.e. 'benzos', 'cannabis', etc
    str sub_category: specific categorization category of the drug i.e. 'pills', 'edibles'
    float price: price of the product in USD
    str shipping_origin: where the product is shipped from (not always the same as origin)
    str ships_to: countries where the product is available
    str inventory_status: in stock, low stock, etc.
    """

    def __init__(self):
        logging.info('----- STARTING WHITEHOUSE MARKET SPIDER -----')
        print('----- STARTING WHITEHOUSE MARKET SPIDER -----')

        self.username = os.environ.get("WHITE_HOUSE_USER")
        self.url = os.environ.get('WHITE_HOUSE_URL')
        self.password = os.environ.get("WHITE_HOUSE_PW")

        self.website = 'White House Market'
        self.table_name = 'narcotics'
        self.process_description = False

        tor_browser_path = os.environ.get("TOR_BROWSER_PATH")

        self.db = DB()

        self.wait_time = 3  # default time the driver will wait for page to load

        try:
            self.driver = TorBrowserDriver(
                tbb_path=tor_browser_path, tbb_logfile_path="./spider_log_verbose.txt")
        except FileNotFoundError:
            print(
                'Error starting tor browser, make sure the path is correct in your .env file')
            exit(0)

        logging.info('\nSuccessfully initialized spider, starting parser\n')
        print('Initializing successful. Starting parser...')
        self.parse()

    def login(self):
        """ Logs into website with login information from .env file
            Terminates program if unsuccessful.
         """

        # get user input if login info not found in .env file
        if not self.username or not self.password:
            print(
                f'Login credentials for {self.website} not found in .env file. You can enter them manually:')
            self.username = input(f'Please enter {self.website} username: ')
            self.password = input(f'Please enter {self.website} password: ')

        # the user must solve captcha then enter a character to continue program
        wait_for_user = input(
            "Enter a character when captcha is solved and page is loaded: ")

        if wait_for_user:

            # handle pop up if needed
            try:
                self.driver.find_element_by_xpath(
                    '/html/body/div[3]/div/form/div/input').click()
            except:
                pass

            # Enter login information
            print("Logging in")
            try:
                self.driver.implicitly_wait(self.wait_time)
                self.driver.find_element_by_xpath(
                    '/html/body/div[3]/form/div[1]/input').send_keys(self.username)
                self.driver.find_element_by_xpath(
                    '/html/body/div[3]/form/div[2]/input').send_keys(self.password)
                self.driver.find_element_by_xpath(
                    '/html/body/div[3]/form/div[4]/input').click()
                self.driver.implicitly_wait(self.wait_time)
                self.driver.find_element_by_xpath(
                    '/html/body/div[3]/div/form/div/div[2]/div/button').click()
                self.driver.implicitly_wait(self.wait_time)
            except:
                print("ERROR LOGGING IN, TERMINATING PROGRAM")
                exit(0)

            print('Login successful')

    def parse(self):
        """ Handles iteration through pages for each of the 50 categories of products"""

        # initial request to website
        self.driver.get(self.url)
        self.login()
        self.driver.implicitly_wait(5)

        # iterate through each category
        for selection in range(1, 50):
            print("Processing: " + self.url+f"/welcome?sc={selection}")
            self.driver.get(self.url+f"/welcome?sc={selection}")

            # each category has a number of pages
            number_of_pages = int(self.driver.find_elements_by_xpath(
                "/html/body/div/div/div/div[@class='panel panel-info']/div/strong")[0].text.split(' ')[-2])

            # iterate through each page for the given category
            for page_number in range(number_of_pages+1):
                self.driver.get(
                    self.url+f"/welcome?sc={selection}&page={page_number}")
                try:
                    self.process_page()
                except Exception as e:
                    logging.error(
                        f'Error processing {self.url}/welcome?sc={selection}&page={page_number}: {e}')

        logging.info('Data extraction completed.')
        print('Data extraction completed. Ending program')
        exit(0)

    def process_page(self):
        """ Processes the products of the current page
            Each product is represented in a dictionary 'item'
         """

        print('Processing products...')

        # ocassionally the last page is empty, skip it
        if not self.driver.find_elements_by_xpath("/html/body/div[4]/div/div/div/div/div/div"):
            return

        #extract the information for each product
        for product in self.driver.find_elements_by_xpath("/html/body/div[4]/div/div/div/div/div/div"):

            text = product.text.split('\n')

            item = {}
            item['website'] = self.website
            item['vendor'] = text[2]
            item['title'] = text[7]

            if len(text[5].split('-', 1)) != 1:
                item['category'] = text[5].split(
                    '-', 1)[0].strip()  # Opiods - Heroin --> Opiods
                item['sub_category'] = text[5].split(
                    '-', 1)[1].strip()  # --Heroin
            else:
                item['category'] = text[5]
                item['sub_category'] = 'Other'

            if text[9][:3] == "USD":
                item['price'] = float(text[9][3:])
            else:
                item['price'] = float(text[10][2:].split()[0])

            item['shipping_origin'] = text[12][12:]
            item['ships_to'] = text[13][10:]
            item['inventory_status'] = text[8]

            #only process description page if explictly needed
            if self.process_description:
                item = self.process_description(product, item)

            item['update_at'] = datetime.datetime.now()

            print(f"\nSuccessfully extracted info for {item['title']}\n")

            # insert item into database
            try:
                self.db.insert(item, self.table_name)
            except Exception as e:
                logging.error(f'Error inserting item into database: {e}')

    def process_description(self, product, item):
        """
        Optional method that parses the description page for a product
        
        This method adds product_description, views, and measurement_unit to the product dictionary item
        
        However, it slows the spider considerably, and will get the account blocked unless the spider is throttled

        :param product: the product whose description page will be extracted
        :param item: the dictionary item representing the product

        """
        print('Processing description page...')

        # go to description page
        try:
            product.find_element_by_xpath('./div/div[2]/a[2]').click()
            description = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
                (By.XPATH, '/html/body/div[4]/div/div/div[4]/div[2]/textarea')))

            #process description if it isn't too long
            if len(description.text) < 998:
                item['product_description'] = description.text
            else:
                item['product_description'] = None

        except TimeoutException as e:
            print('Error processing description page. Moving on without description...')
            logging.error(
                f'Error processing description page for {item["title"]}: {e}')
            return item

        try:
            item['views'] = int(self.driver.find_element_by_xpath(
                '/html/body/div[4]/div/div/div[3]/div[2]/div/div/div[3]/p[6]').text[7:])
            item['measurement_unit'] = self.driver.find_element_by_xpath(
                '/html/body/div[4]/div/div/div[3]/div[2]/div/div/div[3]/p[4]').text[18:]

            description = self.driver.find_element_by_xpath(
                '/html/body/div[4]/div/div/div[4]/div[2]/textarea').text

        except:
            
            item['views'] = None
            item['product_description'] = None
            item['measurement_unit'] = None
            logging.error(
                f'Error processing description page for {item["title"]}: {e}')

        #go back to previous page and resume
        try:
            self.driver.back()
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
                (By.XPATH, '/html/body/div[4]/div/div/div/div/div/div')))
        except TimeoutException:
            pass

        return item
