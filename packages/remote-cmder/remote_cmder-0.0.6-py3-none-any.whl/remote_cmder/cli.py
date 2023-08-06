import argparse
import logging
import socketserver

from .settings import init_settings
from .modules.server import create_cmder_http_request_handler
from .modules.cmder import Cmder
from .modules.cmd import default_cmd_map

init_settings()
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Remote cmder\nexample:\n\tcurl -F 'file=@test.txt' -F 'file=@test.txt' http://127.0.0.1:8888/md5\n",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument("--port", type=int, default=8888)

    args = parser.parse_args()
    port = args.port

    cmder = Cmder()
    cmder.registers(default_cmd_map)
    cmder_http_request_handler = create_cmder_http_request_handler(cmder)
    with socketserver.TCPServer(("", port), cmder_http_request_handler) as httpd:
        logger.info(f"serving at port: {port}")
        httpd.serve_forever()


if __name__ == "__main__":
    main()
