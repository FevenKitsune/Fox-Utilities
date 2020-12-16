import logging

# Set up logger called "discord". Log level is set to INFO.
logger = logging.getLogger("discord")
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())
