import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console = logging.StreamHandler(stream=sys.stdout)
console.setLevel(logging.INFO)
logger.addHandler(console)
