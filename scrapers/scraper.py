import csv 
import time
from tqdm import tqdm # Progress bar
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
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/5\ 37.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        options_chrome.add_argument(f'user-agent={user_agent}')
        options_chrome.add_argument('--window-size=920,1480')
        options_chrome.add_argument('--headless') # Headless mode
        self.driver_chrome = Chrome(driver_path, options=options_chrome)
        self.driver_chrome.get(self.url)
        
        # Wait until webpage is completely loaded (a maximum of 10 secs)
        WebDriverWait(self.driver_chrome, 10).until(visibility_of_element_located((By.XPATH, '//*[@id="site-container"]')))
        
        # Respect crawl delay specified in robots.txt
        time.sleep(10)
        
    def scroll_to_top_player(self):
        '''
        Scroll ranking website until all players are loaded, needed for getting every link.
        '''
        topX_xpath = f'//*[@id="site-container"]/div[4]/div/div[1]/ul/li[{self.topX}]/a/div[1]/div[1]/div[1]'
        topX_found = None
        
        while topX_found == None:
            time.sleep(10)
            self.driver_chrome.execute_script('window.scrollBy(0, 1000)') # Execute JS under the hood...
            try:
                # When topX player web element is found -> exit while loop
                topX_found = WebDriverWait(self.driver_chrome, 2).until(visibility_of_element_located((By.XPATH, topX_xpath)))
            except TimeoutException:
                pass
            
    def get_links(self):
        '''
        Store each player link.
        '''
        self.men_links = []        
        for position in range(1, self.topX + 1):
            player_xpath = f'//*[@id="site-container"]/div[4]/div/div[1]/ul/li[{str(position)}]/a'
            player_element = WebDriverWait(self.driver_chrome, 10).until(visibility_of_element_located((By.XPATH, player_xpath)))
            player_link = player_element.get_attribute('href') # Get player link reference
            self.men_links.append(player_link)
            
        self.women_links = []
        for position in range(1, self.topX + 1):
            player_xpath = f'//*[@id="site-container"]/div[4]/div/div[2]/ul/li[{str(position)}]/a'
            player_element = WebDriverWait(self.driver_chrome, 10).until(visibility_of_element_located((By.XPATH, player_xpath)))
            player_link = player_element.get_attribute('href')
            self.women_links.append(player_link)
            
    def scrap_years(self, link):
        '''
        Scrap matchs/tournaments statistics every available year since 2013 for a given player.
        '''
        years_info = []
        self.driver_chrome.execute_script('window.scrollBy(0, 1000)')
        
        year_selector = self.driver_chrome.find_element_by_xpath('//*[@name="ranking-year"]')
        all_options = year_selector.find_elements_by_tag_name("option")
        
        # Get available years for a scpecific player
        available_years = []
        for year in all_options[1:]:
            available_years.append(year.get_attribute('value'))
        
        
        year_div = 1
        for year in reversed(range(2013, 2021)):
            year_info = []
            
            # Check if year (from 2020 to 2013) is available
            if str(year) in available_years:
                year_selector = self.driver_chrome.find_element_by_class_name('c-form__select-options')
                
                # Run JS for displaying year selector
                self.driver_chrome.execute_script('arguments[0].style.display="block";', year_selector)
                
                year_xpath = f'//*[@id="site-container"]/div[3]/div/div/div/div/div/ul/li[{year_div+1}]'            
                year = self.driver_chrome.find_element_by_xpath(year_xpath)
                
                # Click on year
                ActionChains(self.driver_chrome).move_to_element(year).click().perform()
                
                # Scrap year statistics            
                year_table_xpath = f'//*[@id="site-container"]/div[4]/div[{year_div}]'
            
                played_year_xpath = year_table_xpath + '/div[1]/ul/li[1]/span[2]'
                played_year = WebDriverWait(self.driver_chrome, 30).until(visibility_of_element_located((By.XPATH, played_year_xpath))).text
                year_info.append(played_year)
            
                won_year_xpath = year_table_xpath + '/div[1]/ul/li[2]/span[2]'
                won_year = self.driver_chrome.find_element_by_xpath(won_year_xpath).text
                year_info.append(won_year)
            
                lost_year = int(played_year) - int(won_year)
                year_info.append(lost_year)
                
                # Solve zero division problem
                try:
                    performance_year = int(won_year) / int(played_year)
                except ZeroDivisionError:
                    performance_year = 0
                
                year_info.append(performance_year)
            
                champ_year_xpath = year_table_xpath + '/div[2]/ul/li[1]/span[2]'
                champ_year = self.driver_chrome.find_element_by_xpath(champ_year_xpath).text
                year_info.append(champ_year)
        
                runnerup_year_xpath = year_table_xpath + '/div[2]/ul/li[2]/span[2]'
                runnerup_year = self.driver_chrome.find_element_by_xpath(runnerup_year_xpath).text
                year_info.append(runnerup_year)
                
                year_div += 1
            
            # If year is not available, current year statistics are unknown
            else:
                year_info += ('?' * 6)
                
            years_info += year_info
            
        return years_info
            
    def scrap_player(self, link, ranking):
        '''
        Scrap all player data for a given player, including base info and year statistics.
        '''
        self.driver_chrome.get(link)
        time.sleep(10)
        player_data = []
        
        # Top 1 player has a different web page structure
        if ranking == 1:
            header_xpath = f'//*[@id="site-container"]/div[1]/div/div[1]/div[1]'
        else:
            header_xpath = f'//*[@id="site-container"]/div[1]/div/div[1]/div[2]'
        
        # Scrap player data
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
        player_data.append(court_position)
        
        # Display player personal data by click (and set 10 secs delay).
        personal_data_xpath = '//*[@id="site-container"]/div[1]/div/div[1]/ul/li[2]/a'
        WebDriverWait(self.driver_chrome, 20).until(visibility_of_element_located((By.XPATH, personal_data_xpath))).click()
        time.sleep(10)
    
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
        
        years_info = self.scrap_years(link)
        player_data += years_info
        
        return player_data
        
            
    def start_scraper(self, driver_path, output_file='../dataset/world_padel_tour_dataset.csv'):
        '''
        Start web sraping!
        '''
        start_time = time.time()
        print(f'World Padel Tour Dataset from {self.url}')
        print(f'(!) This process can take about 45 min.')
        
        self.run_driver(driver_path)
        self.scroll_to_top_player()
        self.get_links()
        
        with open(output_file, 'a') as file:
            
            # Player features names
            base_features = [
                'Nombre',
                'Ranking',
                'Puntuacion',
                'Comapanero',
                'Posicion',
                'LugarNacimiento',
                'FechaNacimiento',
                'Altura',
                'Residencia',
                'PartidosJugados',
                'PartidosGanados',
                'PartidosPerdidos',
                'Rendimiento',
                'Racha'
            ]
            
            years_features = []
            
            # Year statistics feature names
            for year in reversed(range(2013, 2021)):
                year_features = []
                year_features += base_features[9:13] + ['Torneos ganados', 'Finales']
                year_features = [str(year) + '_' + feature for feature in year_features]
                years_features += year_features
                
            player_features = base_features + years_features
            player_features.append('Circuito')
            
            # Write features names
            for feature in player_features:
                file.write(feature + ';')
            file.write('\n')
            
            print(f'Scraping top {self.topX} male players info...')

            for ranking, link in enumerate(tqdm(self.men_links), 1): # Display loop progress bar
                player_data = self.scrap_player(link, ranking)
                player_data.append('Masculino')
                for data in player_data:
                    file.write(str(data) + ';')
                file.write('\n')
                
            print(f'Scraping top {self.topX} female players info...')

            
            for ranking, link in enumerate(tqdm(self.women_links), 1):
                player_data = self.scrap_player(link, ranking)
                player_data.append('Femenino')
                for data in player_data:
                    file.write(str(data) + ';')
                file.write('\n')
            
            end_time = time.time()
            elapsed_time = round(((end_time - start_time) / 60) , 2)
            
            print('Scraping was completed.')
            print(f'Elapsed time: {elapsed_time} minutes.')
