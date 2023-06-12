import requests
import time

CACHE_TIMEOUT = 60   # Cache timeout in seconds
cache_expires_at = 0  # When the cache expires
cached_sha = None     # Cached sha value
def get_latest_commit_sha():
    global cache_expires_at, cached_sha
    
    now = time.time()
    if now >= cache_expires_at:
        url = "https://api.github.com/repos/AmoreForever/pc-controller-bot/commits"
        response = requests.get(url)
        if response.status_code == 200:
            if commits := response.json():
                latest_commit = commits[0]
                cached_sha = latest_commit['sha'][:7]
        else:
            cached_sha = None
        
        cache_expires_at = now + CACHE_TIMEOUT
            
    return cached_sha

version = "1 1 4"

print(get_latest_commit_sha())
