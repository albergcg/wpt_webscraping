import sys
sys.path.insert(0, '../')
import scraper

chrome_driver_path = 'D:\Alberto\Archivos de programa\chromedriver.exe'
wpt_scraper = scraper.WPTScraper(topX=50)
wpt_scraper.start_scraper(driver_path=chrome_driver_path)
