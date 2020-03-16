from typing import List

from clai.datasource.action_remote_storage import ActionRemoteStorage
from clai.server.command_message import TerminalReplayMemory, TerminalReplayMemoryComplete
from clai.server.orchestration.orchestrator_provider import OrchestratorProvider


class OrchestratorStorage:
    def __init__(self, orchestrator_provider: OrchestratorProvider, remote_storage: ActionRemoteStorage):
        self._memory: List[TerminalReplayMemoryComplete] = []
        self.orchestrator_provider = orchestrator_provider
        self.remote_storage = remote_storage

    def store_pre(self, replay_pre: TerminalReplayMemory):
        terminal_replay_complete = TerminalReplayMemoryComplete()
        terminal_replay_complete.pre_replay = replay_pre
        self._memory.append(terminal_replay_complete)
        self.__notify_orchestrator(replay_pre)

    def store_post(self, replay_post: TerminalReplayMemory):
        if self._memory:
            self._memory[-1].post_replay = replay_post

    def __notify_orchestrator(self, current_pre: TerminalReplayMemory):
        if len(self._memory) > 1:
            previous_replay = self._memory.pop(0)
            orchestrator = self.orchestrator_provider.get_current_orchestrator()
            orchestrator.record_transition(previous_replay, current_pre)
            self.remote_storage.store(previous_replay.post_replay)
