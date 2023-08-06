# Copyright 2023 OmniSafe Team. All Rights Reserved.
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
"""Implementation of GaussianStdNetActor."""

from typing import List, Optional

import torch
from torch import nn
from torch.distributions import Distribution, Normal

from omnisafe.models.base import Actor
from omnisafe.typing import Activation, InitFunction, OmnisafeSpace
from omnisafe.utils.math import TanhNormal
from omnisafe.utils.model import build_mlp_network


class GaussianSACActor(Actor):
    """Implementation of GaussianSACActor."""

    def __init__(
        self,
        obs_space: OmnisafeSpace,
        act_space: OmnisafeSpace,
        hidden_sizes: List[int],
        activation: Activation = 'relu',
        weight_initialization_mode: InitFunction = 'kaiming_uniform',
    ) -> None:
        super().__init__(obs_space, act_space, hidden_sizes, activation, weight_initialization_mode)
        self.net = build_mlp_network(
            sizes=[self._obs_dim, *self._hidden_sizes, self._act_dim * 2],
            activation=activation,
            weight_initialization_mode=weight_initialization_mode,
        )

        self._current_raw_action: Optional[torch.Tensor] = None
        self.register_buffer('_log2', torch.log(torch.tensor(2.0)))
        self._log2: torch.Tensor

    def _distribution(self, obs: torch.Tensor) -> Distribution:
        mean, log_std = self.net(obs).chunk(2, dim=-1)
        log_std = torch.clamp(log_std, min=-20, max=2)
        std = log_std.exp()
        return Normal(mean, std)

    def predict(self, obs: torch.Tensor, deterministic: bool = False) -> torch.Tensor:
        self._current_dist = self._distribution(obs)
        self._after_inference = True

        if deterministic:
            action = self._current_dist.mean
        else:
            action = self._current_dist.rsample()

        self._current_raw_action = action

        return torch.tanh(action)

    def forward(self, obs: torch.Tensor) -> Distribution:
        self._current_dist = self._distribution(obs)
        self._after_inference = True
        return TanhNormal(self._current_dist.mean, self._current_dist.stddev)

    def log_prob(self, act: torch.Tensor) -> torch.Tensor:
        assert self._after_inference, 'log_prob() should be called after predict() or forward()'
        self._after_inference = False

        if self._current_raw_action is not None:
            logp = self._current_dist.log_prob(self._current_raw_action).sum(axis=-1)
            logp -= (
                2
                * (
                    self._log2
                    - self._current_raw_action
                    - nn.functional.softplus(-2 * self._current_raw_action)
                )
            ).sum(axis=-1)
            self._current_raw_action = None
        else:
            logp = (
                TanhNormal(self._current_dist.mean, self._current_dist.stddev)
                .log_prob(act)
                .sum(axis=-1)
            )

        return logp

    @property
    def std(self) -> float:
        """Get the standard deviation of the normal distribution."""
        return self._current_dist.stddev.mean().item()

    @std.setter
    def std(self, std: float) -> None:
        raise NotImplementedError('GaussianStdNetActor does not support setting std.')
