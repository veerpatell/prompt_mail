from crewai_tools import SerperDevTool, PDFSearchTool, TXTSearchTool, CSVSearchTool, ScrapeWebsiteTool
import os

search_tool = SerperDevTool(api_key=os.getenv("SERPER_API_KEY"))
pdf_tool = PDFSearchTool()
txt_tool = TXTSearchTool()
csv_tool = CSVSearchTool()
scrape_tool = ScrapeWebsiteTool()

ALL_TOOLS = {
    "search_tool": search_tool,
    "pdf_tool": pdf_tool,
    "txt_tool": txt_tool,
    "csv_tool": csv_tool,
    "scrape_tool" : scrape_tool
    }