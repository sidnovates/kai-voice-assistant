from selenium import webdriver
import time
from urllib.parse import quote_plus

# This dictionary maps a domain to its specific search URL structure
# The "{query}" part is a placeholder for the search term
SEARCH_PATTERNS = {
    "youtube.com": "/results?search_query={query}",
    "google.com": "/search?q={query}",
    "amazon.com": "/s?k={query}",
    "wikipedia.org": "/w/index.php?search={query}",
    "stackoverflow.com": "/search?q={query}",
    "github.com": "/search?q={query}"
    # Add any other sites you use often here
}

def open_site(url, request):
    # Step 1: Set up Chrome WebDriver
    driver = webdriver.Chrome()

    # Step 2: If there is no search request, just open the base URL
    if not request:
        print(f"Opening: {url}")
        driver.get(url)
        return

    # Step 3: If there *is* a search request, build the full URL
    
    # Safely encode the search term (e.g., "hello world" -> "hello+world")
    query = quote_plus(request)
    
    target_url = None

    # Find a matching search pattern from our dictionary
    for domain, path_template in SEARCH_PATTERNS.items():
        if domain in url:
            # Build the full URL (e.g., https://youtube.com + /results?search_query=hello+world)
            target_url = url + path_template.format(query=query)
            break
    
    # Step 4: If we didn't find a pattern, just search on Google
    if not target_url:
        print(f"No specific search pattern found for {url}. Defaulting to Google.")
        target_url = f"https://www.google.com/search?q={query}"

    # Step 5: Open the final, constructed URL
    print(f"Opening: {target_url}")
    driver.get(target_url)

    # We no longer need the rest of the old code (find_element, send_keys, etc.)