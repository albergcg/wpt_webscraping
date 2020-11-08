import sys
sys.path.append(0, '../')
import scraper

wpt_scraper = scraper.WPTScraper(topX=100)
wpt_scraper.start_scraper()
