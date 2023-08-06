import os

STORAGE_DIR_PATH = os.getenv(
    "REMOTE_CMDER_STORAGE_DIR_PATH", default="./.remote_cmder_storage"
)
