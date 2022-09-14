import logging, datetime, platform, os, socket
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
            logging.FileHandler("debug.log"),
            logging.StreamHandler()
        ])

logger = logging.getLogger(__name__)


header = f"""

Remote Macro Control Host Version: 0.01
Python Version: {platform.python_version()}
OS: {platform.platform()}
Date : {datetime.datetime.now()}
Hostname: {socket.gethostname()}
Ip: {socket.gethostbyname(socket.gethostname())}
{30*"_"}
"""

logger.info(header)