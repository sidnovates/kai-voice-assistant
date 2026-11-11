import webbrowser
from urllib.parse import quote_plus, urlparse
from speak import speak

# Allowlist of acceptable URL schemes
ALLOWED_SCHEMES = {"http", "https"}

# This dictionary maps a domain to its specific search URL structure
SEARCH_PATTERNS = {
    "youtube.com": "/results?search_query={query}",
    "google.com": "/search?q={query}",
    "amazon.com": "/s?k={query}",
    "wikipedia.org": "/w/index.php?search={query}",
    "stackoverflow.com": "/search?q={query}",
    "github.com": "/search?q={query}",
    "reddit.com": "/search/?q={query}",
    "twitter.com": "/search?q={query}",
    "x.com": "/search?q={query}"
}

def is_safe_url(url):
    """Validates that a URL uses safe protocols and is not targeting local internal endpoints."""
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ALLOWED_SCHEMES:
            return False
        if not parsed.netloc:
            return False
        # Block localhost / internal loopback destinations
        host = parsed.netloc.split(":")[0].lower()
        if host in {"localhost", "127.0.0.1", "0.0.0.0", "::1"}:
            return False
        return True
    except Exception:
        return False

def open_site(url, request):
    # Ensure scheme exists
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    # Step 1: Validate URL safety and allowlist rules
    if not is_safe_url(url):
        print(f"Rejected unsafe or invalid URL: {url}")
        speak("Sorry, that website destination is not permitted.")
        return

    # Step 2: If there is no search request, open the base URL
    if not request:
        print(f"Opening: {url}")
        webbrowser.open(url)
        return

    # Step 3: If there is a search request, build the full URL
    query = quote_plus(request)
    target_url = None

    for domain, path_template in SEARCH_PATTERNS.items():
        if domain in url:
            target_url = url.rstrip("/") + path_template.format(query=query)
            break

    # Step 4: If no specific pattern found, default to Google search
    if not target_url:
        print(f"No specific search pattern found for {url}. Defaulting to Google search.")
        target_url = f"https://www.google.com/search?q={query}"

    # Step 5: Final safety check and open with default browser (no cold-start or resource leaks)
    if is_safe_url(target_url):
        print(f"Opening safely via default browser: {target_url}")
        webbrowser.open(target_url)
    else:
        speak("Constructed search URL failed safety checks.")