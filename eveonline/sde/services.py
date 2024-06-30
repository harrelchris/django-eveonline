import urllib.request


def get_remote_hash() -> str:
    request = urllib.request.Request(
        url="https://www.fuzzwork.co.uk/dump/sqlite-latest.sqlite.bz2.md5",
    )
    response = urllib.request.urlopen(request)
    content = response.read()
    return content.decode("utf-8").strip()
