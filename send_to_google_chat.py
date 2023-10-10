#send_to_google_chat.py
import requests
from configparser import ConfigParser
import logging  # Import logging
from log_handler import initialize_logging 

logger = logging.getLogger(__name__)

def send_to_google_chat(message, webhook_url):  # webhook_url added as parameter
    logger.info(f"Sending message to Google Chat: {message}")  # Log message
    payload = {
        "text": message
    }
    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 200:
            logger.info("Successfully sent message to Google Chat")
        else:
            logger.warning(f"Failed to send message to Google Chat. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred while sending message to Google Chat: {e}")
