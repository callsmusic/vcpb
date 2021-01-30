"""

A simple Python class written for VCPB for playing audio with MPlayer.

"""
import os
import subprocess

__author__ = "Roj Serbest <rojserbest@icloud.com>"
__all__ = ("PyMPlayer", "State")


class State:
    NOTHING = "NOTHING"
    PLAYING = "PLAYING"
    PAUSED = "PAUSED"


class PyMPlayer:
    def __init__(self, pipe="mp_pipe"):
        try:
            os.mkfifo(pipe)
        except:
            pass

        self.pipe = pipe
        self.process = None
        self._set_state(State.NOTHING)

    def _run_command(self, command):
        os.system(f'echo "{command}" > {self.pipe}')

    def _set_state(self, state):
        self._state = state

    def get_state(self):
        if self.process:
            if self.process.poll() != None:
                self.process = None
                self._set_state(State.NOTHING)
                return State.NOTHING

        return self._state

    def play(self, file):
        self.file = file
        self.process = subprocess.Popen(
            [
                "mplayer",
                "-novideo",
                "-input",
                f"file={self.pipe}",
                self.file
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=False
        )
        self._set_state(State.PLAYING)

    def pause(self):
        if self.get_state() == State.PLAYING:
            self._run_command("pause")
            self._set_state(State.PAUSED)
            return True

    def resume(self):
        if self.get_state() == State.PAUSED:
            self._run_command("pause")
            self._set_state(State.PLAYING)
            return True

    def seek_forward(self, seconds: int):
        if self.get_state() in (State.PLAYING, State.PAUSED):
            self._run_command(f"seek +{seconds}")
            return True

    def seek_backward(self, seconds: int):
        if self.get_state() in (State.PLAYING, State.PAUSED):
            self._run_command(f"seek -{seconds}")
            return True

    def quit(self):
        if self.process:
            if self.process.poll() == None:
                self._run_command("quit")
                return True

    def wait_until_ends(self):
        if self.process:
            return self.process.wait()
