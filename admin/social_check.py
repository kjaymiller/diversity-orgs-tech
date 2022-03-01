social_checkers = {
    "facebook": "facebook.com",
    "instagram": "instagram.com",
    "twitter": "twitter.com",
    "linkedin": "linkedin.com",
    "meetup": "meetup.com",
    "github": "github.com",
    "youtube": "youtube.com",
    "snapchat": "snapchat.com",
    "tiktok": "tiktok.com",
    "eventbrite": "eventbrite.com",
}


def social_check(url):
    """
    Checks if the url matches any of the social social_cards
    """
    for k, v in social_checkers.items():
        if v in url:
            return {k: url}
    return {"url": url}
