from fastmcp import FastMCP
from typing import Dict
from dotenv import load_dotenv
import httpx
import os
import json
import logging
import sys

load_dotenv()

logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(name)s:%(message)s",
)

mcp = FastMCP(name="Job Search MCP Server")

JOOBLE_API_KEY = os.getenv("JOOBLE_API_KEY")

BASE_URL = f"https://jooble.org/api/{JOOBLE_API_KEY}"


async def make_requests(url: str, body: dict):
    """Make a search request to the url provided"""

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                url,
                content=json.dumps(body),
                headers={"Content-Type": "application/json"},
                timeout=30,
            )
            response.raise_for_status()
            return response.json()

        except httpx.HTTPStatusError as e:
            return {"error": f"API Request failed {e.response.text}"}
        except Exception as e:
            return {"error": str(e)}


@mcp.tool()
async def search_jobs(role: str, location: str) -> Dict[str, any] | None:
    """
    Search for job openings on Jooble with role and location
    Args:
        role: Job role you are looking for
        location: Location for job search
    """

    body = {"keywords": role, "location": location}

    response = await make_requests(BASE_URL, body)

    return response


if __name__ == "__main__":
    mcp.run()
