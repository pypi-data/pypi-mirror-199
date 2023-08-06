class NotSetEmail(Exception):
    """You have not set up mail"""


class ProblemWithGetEmail(Exception):
    """Problem receiving email"""


class CloudflareDetect(Exception):
    """Detect Cloudflare protection"""
