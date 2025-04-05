from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup

app = FastAPI(title="ShopScraperAPI")

# CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/search/aliexpress")
def search_aliexpress(query: str = Query(..., description="Search term")):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    }
    search_url = f"https://www.aliexpress.com/wholesale?SearchText={query.replace(' ', '+')}"

    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
        return {"error": "Failed to fetch results"}

    soup = BeautifulSoup(response.text, "html.parser")
    products = []

    for item in soup.select(".manhattan--container--1lP57Ag")[:10]:  # Limit to first 10
        title_elem = item.select_one(".manhattan--titleText--WccSjUS")
        price_elem = item.select_one(".manhattan--price-sale--1CCSZfK")
        link_elem = item.find("a", href=True)

        if title_elem and price_elem and link_elem:
            products.append({
                "title": title_elem.text.strip(),
                "price": price_elem.text.strip(),
                "link": f"https:{link_elem['href']}"
            })

    return {"results": products}

