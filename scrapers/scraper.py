import csv
import time
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException

class WPTScraper():
    '''
    Scrape World Padel Tour player dataset.
    '''
    
    def __init__(self, topX):
        '''
        Instantiate a WPTScraper object ready to be used!
        '''
        self.topX = topX
        self.url = 'https://www.worldpadeltour.com/jugadores'
        self.data = []
        
    def run_driver(self, driver_path):
        '''
        Run Chrome driver in headless mode (without UI -> faster).
        '''
        options_chrome = Options()
        options_chrome.add_argument('--window-size=920,1480')
        options_chrome.add_argument('--headless') # Headless mode
        self.driver_chrome = Chrome(driver_path, options=options_chrome)
        self.driver_chrome.get(self.url)
        
        # Wait until webpage is completely loaded (a maximum of 10 secs)
        WebDriverWait(self.driver_chrome, 10).until(visibility_of_element_located((By.XPATH, '//*[@id="site-container"]')))
        
    def scroll_to_top_player(self):
        '''
        Scroll ranking website until all players are visible, needed for getting every link.
        '''
        topX_xpath = f'//*[@id="site-container"]/div[4]/div/div[1]/ul/li[{self.topX}]/a/div[1]/div[1]/div[1]'
        topX_found = None
        
        while topX_found == None:
            self.driver_chrome.execute_script('window.scrollBy(0, 1000)') # Execute JS under the hood...
            try:
                # When topX player web element is found -> exit while loop
                topX_found = WebDriverWait(self.driver_chrome, 2).until(visibility_of_element_located((By.XPATH, topX_xpath)))
            except TimeoutException:
                pass
            
    def get_links(self):
        '''
        Store each player link inside a list.
        '''
        self.men_links = []        
        for position in range(1, self.topX + 1):
            player_xpath = f'//*[@id="site-container"]/div[4]/div/div[1]/ul/li[{str(position)}]/a'
            player_element = WebDriverWait(self.driver_chrome, 10).until(visibility_of_element_located((By.XPATH, player_xpath)))
            player_link = player_element.get_attribute('href')
            self.men_links.append(player_link)
            
        self.women_links = []
        for position in range(1, self.topX + 1):
            player_xpath = f'//*[@id="site-container"]/div[4]/div/div[2]/ul/li[{str(position)}]/a'
            player_element = WebDriverWait(self.driver_chrome, 10).until(visibility_of_element_located((By.XPATH, player_xpath)))
            player_link = player_element.get_attribute('href')
            self.women_links.append(player_link)
            
    def scrap_years(self, link):
       '''
       Scrap matchs/tournaments statistics every year since 2013 for a given player.
       '''
        years_info = []
        driver_chrome.execute_script('window.scrollBy(0, 1000)')
        
        for year_div in range(1, 9):
            
            year_selector = self.driver_chrome.find_element_by_class_name('c-form__select-options')
            self.driver_chrome.execute_script('arguments[0].style.display="block";', year_selector)
            year_xpath = f'//*[@id="site-container"]/div[3]/div/div/div/div/div/ul/li[{year_div+1}]'            
            year = driver_chrome.find_element_by_xpath(year_xpath)
            ActionChains(driver_chrome).move_to_element(year).click().perform()
            
            year_table_xpath = f'//*[@id="site-container"]/div[4]/div[{year_div}]'
            
            played_year_xpath = year_table_xpath + "/div[1]/ul/li[1]/span[2]"
            played_year = WebDriverWait(self.driver_chrome, 30).until(visibility_of_element_located((By.XPATH, played_year_xpath))).text
            years_info.append(played_year)
            
    def scrap_player(self, link, ranking):
        self.driver_chrome.get(link)        
        player_data = []
        if ranking == 1:
            header_xpath = f'//*[@id="site-container"]/div[1]/div/div[1]/div[1]'
        else:
            header_xpath = f'//*[@id="site-container"]/div[1]/div/div[1]/div[2]'
        
        name_xpath = header_xpath + '/div/h1'
        name = WebDriverWait(self.driver_chrome, 3).until(visibility_of_element_located((By.XPATH, name_xpath))).text
        player_data.append(name)
        
        ranking_xpath = header_xpath + '/div/div/div[1]/p[2]'
        ranking = WebDriverWait(self.driver_chrome, 3).until(visibility_of_element_located((By.XPATH, ranking_xpath))).text    
        player_data.append(ranking)
    
        points_xpath = header_xpath + '/div/div/div[2]/p[2]'
        points = WebDriverWait(self.driver_chrome, 3).until(visibility_of_element_located((By.XPATH, points_xpath))).text
        player_data.append(points)
    
        mate_xpath = '//*[@id="site-container"]/div[1]/div/div[2]/div[2]/ul[1]/li[1]/p/a'
        mate = WebDriverWait(self.driver_chrome, 3).until(visibility_of_element_located((By.XPATH, mate_xpath))).text
        player_data.append(mate)
    
        position_xpath = '//*[@id="site-container"]/div[1]/div/div[2]/div[2]/ul[1]/li[2]/p'
        court_position = WebDriverWait(self.driver_chrome, 3).until(visibility_of_element_located((By.XPATH, position_xpath))).text
        player_data.append(court)
    
        personal_data_xpath = '//*[@id="site-container"]/div[1]/div/div[1]/ul/li[2]/a'
        WebDriverWait(self.driver_chrome, 20).until(visibility_of_element_located((By.XPATH, personal_data_xpath))).click()
    
        birthplace_xpath = '//*[@id="site-container"]/div[1]/div/div[2]/div[2]/ul[2]/li[1]/p'
        birthplace = WebDriverWait(self.driver_chrome, 3).until(visibility_of_element_located((By.XPATH, birthplace_xpath))).text
        player_data.append(birthplace)
    
        birthdate_xpath = '//*[@id="site-container"]/div[1]/div/div[2]/div[2]/ul[2]/li[2]/p'
        birthdate = WebDriverWait(self.driver_chrome, 30).until(visibility_of_element_located((By.XPATH, birthdate_xpath))).text
        player_data.append(birthdate)
    
        height_xpath = '//*[@id="site-container"]/div[1]/div/div[2]/div[2]/ul[2]/li[3]/p'
        height = WebDriverWait(self.driver_chrome, 30).until(visibility_of_element_located((By.XPATH, height_xpath))).text
        player_data.append(height)
    
        residence_xpath = '//*[@id="site-container"]/div[1]/div/div[2]/div[2]/ul[2]/li[4]/p'
        residence = WebDriverWait(self.driver_chrome, 30).until(visibility_of_element_located((By.XPATH, residence_xpath))).text
        player_data.append(residence)
    
        played_xpath = '//*[@id="site-container"]/div[2]/div/div/div[1]/p[2]'
        played = WebDriverWait(self.driver_chrome, 30).until(visibility_of_element_located((By.XPATH, played_xpath))).text
        player_data.append(played)
    
        won_xpath = '//*[@id="site-container"]/div[2]/div/div/div[2]/p[2]'
        won = WebDriverWait(self.driver_chrome, 30).until(visibility_of_element_located((By.XPATH, won_xpath))).text
        player_data.append(won)
    
        lost = int(played) - int(won)
        player_data.append(lost)
        
        performance = int(won) / int(played)
        player_data.append(performance)
        
        consecutive_xpath = '//*[@id="site-container"]/div[2]/div/div/div[5]/p[2]'
        consecutive = WebDriverWait(self.driver_chrome, 30).until(visibility_of_element_located((By.XPATH, consecutive_xpath))).text
        player_data.append(consecutive)
        
            
    def start_scraper(self):
        self.init_driver("D:\Alberto\Archivos de programa\chromedriver.exe")
        self.scroll_to_top_player()
        self.get_links()
        
        for link in self.men_links:
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        