# Copyright 2022-2023 OmniSafe Team. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Abstract base class for buffer."""

from abc import ABC, abstractmethod
from typing import Dict

import torch
from gymnasium.spaces import Box

from omnisafe.typing import OmnisafeSpace


class BaseBuffer(ABC):
    """Abstract base class for buffer."""

    def __init__(
        self,
        obs_space: OmnisafeSpace,
        act_space: OmnisafeSpace,
        size: int,
        device: torch.device = torch.device('cpu'),
    ):
        """Initialize the buffer."""
        if isinstance(obs_space, Box):
            obs_buf = torch.zeros((size, *obs_space.shape), dtype=torch.float32, device=device)
        else:
            raise NotImplementedError
        if isinstance(act_space, Box):
            act_buf = torch.zeros((size, *act_space.shape), dtype=torch.float32, device=device)
        else:
            raise NotImplementedError

        self.data: Dict[str, torch.Tensor] = {
            'obs': obs_buf,
            'act': act_buf,
            'reward': torch.zeros(size, dtype=torch.float32, device=device),
            'cost': torch.zeros(size, dtype=torch.float32, device=device),
            'done': torch.zeros(size, dtype=torch.float32, device=device),
        }
        self._size = size
        self._device = device

    @property
    def device(self) -> torch.device:
        """Return the device of the buffer."""
        return self._device

    @property
    def size(self) -> int:
        """Return the size of the buffer."""
        return self._size

    def __len__(self):
        """Return the length of the buffer."""
        return self._size

    def add_field(self, name: str, shape: tuple, dtype: torch.dtype):
        """Add a field to the buffer."""
        self.data[name] = torch.zeros((self._size, *shape), dtype=dtype, device=self._device)

    @abstractmethod
    def store(self, **data: torch.Tensor):
        """Store a transition in the buffer."""
