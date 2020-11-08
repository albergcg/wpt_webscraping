import sys
sys.path.append(0, '../')
import scraper

chrome_driver_path = 'D:\Alberto\Archivos de programa\chromedriver.exe'
wpt_scraper = scraper.WPTScraper(topX=100)
wpt_scraper.start_scraper()
