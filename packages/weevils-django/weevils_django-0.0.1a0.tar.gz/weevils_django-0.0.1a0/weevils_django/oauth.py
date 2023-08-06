from social_core.backends.oauth import BaseOAuth2

class WeevilsOAuth(BaseOAuth2):
    """
    Authentication backend to use weevils.io to login users through Github, BitBucket etc
    """

    name = "weevils"
