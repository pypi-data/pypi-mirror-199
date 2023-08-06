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
"""Environments in the Safety Gymnasium."""


from typing import Any, Dict, Optional, Tuple

import numpy as np
import safety_gymnasium
import torch

from omnisafe.envs.core import CMDP, env_register


@env_register
class SafetyGymnasiumEnv(CMDP):
    """Safety Gymnasium environment."""

    _support_envs = [
        'SafetyPointGoal0-v0',
        'SafetyPointGoal1-v0',
        'SafetyPointGoal2-v0',
        'SafetyPointButton0-v0',
        'SafetyPointButton1-v0',
        'SafetyPointButton2-v0',
        'SafetyPointPush0-v0',
        'SafetyPointPush1-v0',
        'SafetyPointPush2-v0',
        'SafetyPointCircle0-v0',
        'SafetyPointCircle1-v0',
        'SafetyPointCircle2-v0',
        'SafetyCarGoal0-v0',
        'SafetyCarGoal1-v0',
        'SafetyCarGoal2-v0',
        'SafetyCarButton0-v0',
        'SafetyCarButton1-v0',
        'SafetyCarButton2-v0',
        'SafetyCarPush0-v0',
        'SafetyCarPush1-v0',
        'SafetyCarPush2-v0',
        'SafetyCarCircle0-v0',
        'SafetyCarCircle1-v0',
        'SafetyCarCircle2-v0',
        'SafetyAntGoal0-v0',
        'SafetyAntGoal1-v0',
        'SafetyAntGoal2-v0',
        'SafetyAntButton0-v0',
        'SafetyAntButton1-v0',
        'SafetyAntButton2-v0',
        'SafetyAntPush0-v0',
        'SafetyAntPush1-v0',
        'SafetyAntPush2-v0',
        'SafetyAntCircle0-v0',
        'SafetyAntCircle1-v0',
        'SafetyAntCircle2-v0',
        'SafetyHalfCheetahVelocity-v4',
        'SafetyHopperVelocity-v4',
        'SafetySwimmerVelocity-v4',
        'SafetyWalker2dVelocity-v4',
        'SafetyAntVelocity-v4',
        'SafetyHumanoidVelocity-v4',
    ]
    need_auto_reset_wrapper = False
    need_time_limit_wrapper = False

    def __init__(
        self, env_id: str, num_envs: int = 1, device: torch.device = torch.device('cpu'), **kwargs
    ) -> None:
        super().__init__(env_id)
        if num_envs > 1:
            self._env = safety_gymnasium.vector.make(env_id=env_id, num_envs=num_envs, **kwargs)
            self._action_space = self._env.single_action_space
            self._observation_space = self._env.single_observation_space
        else:
            self._env = safety_gymnasium.make(id=env_id, autoreset=True, **kwargs)
            self._action_space = self._env.action_space
            self._observation_space = self._env.observation_space

        self._num_envs = num_envs
        self._metadata = self._env.metadata
        self._device = device

    def step(
        self, action: torch.Tensor
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor, Dict]:
        obs, reward, cost, terminated, truncated, info = self._env.step(
            action.detach().cpu().numpy()
        )
        obs, reward, cost, terminated, truncated = map(
            lambda x: torch.as_tensor(x, dtype=torch.float32, device=self._device),
            (obs, reward, cost, terminated, truncated),
        )
        if 'final_observation' in info:
            info['final_observation'] = np.array(
                [
                    array if array is not None else np.zeros(obs.shape[-1])
                    for array in info['final_observation']
                ]
            )
            info['final_observation'] = torch.as_tensor(
                info['final_observation'], dtype=torch.float32, device=self._device
            )

        return obs, reward, cost, terminated, truncated, info

    def reset(self, seed: Optional[int] = None) -> Tuple[torch.Tensor, Dict]:
        obs, info = self._env.reset(seed=seed)
        return torch.as_tensor(obs, dtype=torch.float32, device=self._device), info

    def set_seed(self, seed: int) -> None:
        self.reset(seed=seed)

    def sample_action(self) -> torch.Tensor:
        return torch.as_tensor(
            self._env.action_space.sample(), dtype=torch.float32, device=self._device
        )

    def render(self) -> Any:
        return self._env.render()

    def close(self) -> None:
        self._env.close()
