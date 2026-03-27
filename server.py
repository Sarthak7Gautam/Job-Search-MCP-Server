from fastmcp import FastMCP
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from typing import Dict
import httpx
import os

mcp = FastMCP(name="Job Search MCP Server")

load_dotenv()

JOOBLE_API_KEY = os.getenv("JOOBLE_API_KEY")

BASE_URL = f"https://api.jooble.org/api/{JOOBLE_API_KEY}"


async def make_requests(url: str):
    """Make a job request to the url provided"""

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=30)
            response.raise_for_status()
            return response.json()

        except httpx.HTTPStatusError as e:
            return {"error": f"API Request failed {e.response.text}"}
        except Exception as e:
            return {"error": e}


@mcp.tool()
async def search_jobs(role: str, location: str) -> Dict[str, any] | None:
    """
    Search for job openings on Jooble with role and location
    Args:
        role: Job role you are looking for
        location: Location for job search
    """

    url = f"{BASE_URL}/searchjobs?keyword={role}&location={location}"

    response = await make_requests(url)

    return response


llm = ChatGroq(model_name="llama-3.3-70B-versatile")

result = llm.invoke("Hello")

if __name__ == "__main__":
    mcp.run()
