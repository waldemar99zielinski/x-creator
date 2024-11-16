import os
from dotenv import load_dotenv

from crewai_tools import (
    FirecrawlSearchTool,
    FirecrawlCrawlWebsiteTool,
    FirecrawlScrapeWebsiteTool,
    ScrapeElementFromWebsiteTool,
    ScrapeWebsiteTool,
    SerperDevTool
)

load_dotenv()

# TODO move to a config file
serper_api_key = os.getenv("SERPER_API_KEY")

if not serper_api_key:
    raise ValueError("Missing Serper API keys in environment variables")

firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY")

if not firecrawl_api_key:
    raise ValueError("Missing Firecrawl API keys in environment variables")


class BrowserTools():
    def __init__(self):
        self.firecrawl_search_tool = FirecrawlSearchTool()
        self.firecrawl_crawl_tool = FirecrawlCrawlWebsiteTool()
        self.firecrawl_scrape_tool = FirecrawlScrapeWebsiteTool()
        self.scrape_element_tool = ScrapeElementFromWebsiteTool()
        self.scrape_website_tool = ScrapeWebsiteTool()
        self.serper_tool = SerperDevTool()

    def get_all_tools(self):
        return [
            # self.firecrawl_search_tool,
            # self.firecrawl_crawl_tool,
            # self.firecrawl_scrape_tool,
            self.scrape_element_tool,
            self.scrape_website_tool,
            self.serper_tool,
        ]
