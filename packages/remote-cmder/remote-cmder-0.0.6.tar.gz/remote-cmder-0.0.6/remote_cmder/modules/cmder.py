from dataclasses import dataclass

from remote_cmder.core.enums import ResponseType


class Cmder:
    def __init__(self):
        self.__cmd_map = {}

    def execute(self, cmd, filename, data, *args, **kwargs):
        return self.__cmd_map[cmd](filename, data, *args, **kwargs)

    def is_cmd_supported(self, cmd):
        return cmd in self.__cmd_map

    def register(self, cmd, func):
        self.__cmd_map[cmd] = func

    def registers(self, cmd_map):
        self.__cmd_map.update(cmd_map)


@dataclass
class CmderResponse:
    result: bool
    data: bytes
    type: ResponseType
