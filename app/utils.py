import urllib

from app import app, hashids

def transform_url(input_url):
    return urllib.parse.urljoin(
        app.config["BASE_URL"],
        hashids.encode(input_url)
    )
