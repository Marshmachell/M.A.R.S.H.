import os
import logging
from logging.config import dictConfig
from dotenv import load_dotenv

load_dotenv()

DISCORD_API_SECRET = os.getenv("DISCORD_API_TOKEN")
FUN_AI_TOKEN = os.getenv("FUN_AI_TOKEN")
FUN_AI_CHARACTER_ID = os.getenv("FUN_AI_CHARACTER_ID")
FUN_AI_VOICE_ID = os.getenv("FUN_AI_VOICE_ID")
COMMAND_PREFIX = os.getenv("COMMAND_PREFIX")
AUTHORIZED_IDs = [
    539054518885679126,
    1153737024432513056,
    482996094591041536,
    884798400258793483
]

TEST_AI_TOKEN = '94effeb9586d1b9947dd40635301f73a279cdf88'
TEST_AI_CHAR = 'linRU19YoDFePwwf-Xp9gD_FknrCHankrwpOsMc9t30'
TEST_AI_VOICE = '7fa1ca50-868e-44bf-9443-3f43e2bee018'

LOGGING_CONFIG = {
    "version": 1,
    "disabled_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)-10s - %(asctime)s - %(module)-15s : %(message)s"
        },
        "standard": {
            "format": "%(levelname)-10s - %(name)-15s : %(message)s"
        }
    },
    "handlers": {
        "console": {
            'level': "DEBUG",
            'class': "logging.StreamHandler",
            'formatter': "standard"
        },
        "console2": {
            'level': "WARNING",
            'class': "logging.StreamHandler",
            'formatter': "standard"
        },
        "file": {
            'level': "INFO",
            'class': "logging.FileHandler",
            'filename': "logs/infos.log",
            'mode': "w",
            'formatter': "verbose"
        }
    },
    "loggers": {
        "bot": {
            'handlers': ['console'],
            "level": "INFO",
            "propagate": False
        },
        "discord": {
            'handlers': ['console2', "file"],
            "level": "INFO",
            "propagate": False
        }
    }
}
dictConfig(LOGGING_CONFIG)