import re

def is_valid_youtube_url(url):
    # Regular expression pattern for YouTube URLs
    youtube_url_pattern = re.compile(
        r'(https?://)?(www\.)?(youtube\.com|youtu\.?be)/.+'
    )
    
    # Check if the URL matches the pattern
    if youtube_url_pattern.match(url):
        return True
    else:
        return False
