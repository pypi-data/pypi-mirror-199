from abc import ABC, abstractmethod
from loguru import logger

from .pboc import PBOC
from .bc_info import BCInfo


class BCReader(ABC):
    @abstractmethod
    def open(self) -> None:
        pass

    @abstractmethod
    def detect(self) -> None:
        pass

    @abstractmethod
    def prepare(self) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass

    @abstractmethod
    def read_info(self, amount: int, trade: str, merchant: str = "") -> BCInfo:
        pass

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.close()
        except Exception as e:
            logger.debug(e)


class CPUReader(BCReader):
    @abstractmethod
    def run(self, hex_cmd: str) -> str:
        pass


class RFCPUReader(CPUReader):
    def read_info(self, amount: int, trade: str, merchant: str = "") -> BCInfo:
        raise NotImplementedError()


class SmartReader(CPUReader):
    def read_info(self, amount: int, trade: str, merchant: str = "") -> BCInfo:
        _pboc = PBOC(self.run)
        return _pboc.read_info(amount, trade, merchant)
