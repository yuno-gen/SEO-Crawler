import argparse
import sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def main():
    parser = argparse.ArgumentParser(description="Run SEO Scrapy crawler")
    parser.add_argument('--start-url', type=str, required=True, help="URL to start crawling")
    parser.add_argument('--project', type=str, required=True, help="Project/domain identifier")
    args = parser.parse_args()

    # You might want to set settings here dynamically
    settings = get_project_settings()
    # If you need to pass settings (e.g., project), do it here:
    settings.set('START_URL', args.start_url)
    settings.set('PROJECT_ID', args.project)

    process = CrawlerProcess(settings)
    # Import the spider dynamically, if named e.g., 'generic_site'
    try:
        from spiders.generic_site import GenericSiteSpider
    except ImportError:
        print("Could not import GenericSiteSpider. Is your Scrapy spider in spiders/generic_site.py?", file=sys.stderr)
        sys.exit(1)
    
    process.crawl(GenericSiteSpider, start_url=args.start_url, project=args.project)
    process.start()

if __name__ == "__main__":
    main()
