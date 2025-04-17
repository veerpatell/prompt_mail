from crewai_tools import SerperDevTool, PDFSearchTool, TXTSearchTool, CSVSearchTool
pdf_tool = PDFSearchTool()
search_tool = SerperDevTool(api_key=os.getenv("SERPER_API_KEY"))
txt_tool = TXTSearchTool()
csv_tool = CSVSearchTool()
ALL_TOOLS = {
        "search_tool": SerperDevTool(api_key=os.getenv("SERPER_API_KEY")),
        "pdf_tool": PDFSearchTool(),
        "txt_tool": TXTSearchTool(),
        "csv_tool": CSVSearchTool()
    }