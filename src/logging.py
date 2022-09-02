'''
        Instead of printing the "logs" with built-in print(),
        logging module provides healthier solution.
'''



import logging


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger()

