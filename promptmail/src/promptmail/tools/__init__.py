from crewai_tools import SerperDevTool, PDFSearchTool, TXTSearchTool, CSVSearchTool
def get_tools(self, agent_id: str) -> list:
    ALL_TOOLS = {
        "search_tool": SerperDevTool(api_key=os.getenv("SERPER_API_KEY")),
        "pdf_tool": PDFSearchTool(),
        "txt_tool": TXTSearchTool(),
        "csv_tool": CSVSearchTool()
    }

    if agent_id == "manager":
        return [ALL_TOOLS["search_tool"]]
    elif agent_id == "researcher":
        return [ALL_TOOLS["pdf_tool"], ALL_TOOLS["txt_tool"], ALL_TOOLS["csv_tool"]]
    elif agent_id == "scheduler":
        return [ALL_TOOLS["csv_tool"]]
    return []