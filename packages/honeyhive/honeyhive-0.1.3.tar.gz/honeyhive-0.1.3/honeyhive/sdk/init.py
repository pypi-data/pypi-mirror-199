from honeyhive.api.client import HoneyHive, get_client
from typing import Dict, Optional
import honeyhive

def honeyhive_client() -> HoneyHive:
    """Get a HoneyHive client"""
    return get_client("https://honeyhive.ai:5000/", honeyhive.api_key)