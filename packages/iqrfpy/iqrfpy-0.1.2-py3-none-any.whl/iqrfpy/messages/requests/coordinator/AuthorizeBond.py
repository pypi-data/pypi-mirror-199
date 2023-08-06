from __future__ import annotations
from typeguard import typechecked
from uuid import uuid4
from typing import List, Optional, Union
from iqrfpy.enums.Commands import CoordinatorRequestCommands
from iqrfpy.enums.MessageTypes import CoordinatorMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.utils.common import Common
from iqrfpy.messages.requests.IRequest import IRequest

__all__ = ['AuthorizeBondRequest']


@typechecked
class AuthorizeBondRequest(IRequest):

    def __init__(self, nodes: Optional[List[dict]], hwpid: int = Common.HWPID_MAX, msgid: str = str(uuid4())):
        super().__init__(
            nadr=0,
            pnum=EmbedPeripherals.COORDINATOR,
            pcmd=CoordinatorRequestCommands.AUTHORIZE_BOND,
            m_type=CoordinatorMessages.AUTHORIZE_BOND,
            hwpid=hwpid,
            msgid=msgid
        ),
        self._nodes: List[dict] = nodes
        self._validate()

    def _validate(self) -> None:
        if len(self._nodes) == 0:
            raise ValueError('At least one pair of requested address and MID is required.')
        if len(self._nodes) > 11:
            raise ValueError('Request can carry at most 11 pairs of address and MID.')

    def set_nodes(self, nodes: List[int]) -> None:
        self._nodes = nodes

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        self._validate()
        pdata = []
        for node in self._nodes:
            pdata.append(node['reqAddr'])
            pdata.append((node['mid'] >> 24) & 0xFF)
            pdata.append((node['mid'] >> 16) & 0xFF)
            pdata.append((node['mid'] >> 8) & 0xFF)
            pdata.append(node['mid'] & 0xFF)
        self._pdata = pdata
        return super().to_dpa(mutable=mutable)

    def to_json(self) -> dict:
        self._validate()
        self._params = {'nodes': self._nodes}
        return super().to_json()
