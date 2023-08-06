import os
import random
from datetime import date
from neon_solvers import AbstractSolver
from os import listdir, remove as remove_file
from os.path import dirname, isfile
from os.path import join, dirname
from ovos_utils.log import LOG


class FailureSolver(AbstractSolver):
    def __init__(self):
        super().__init__(name="FailureBot", priority=999, enable_cache=False, enable_tx=False)

    # officially exported Solver methods
    def get_spoken_answer(self, query, context=None):
        context = context or {}
        lang = context.get("lang") or "en-us"
        lines = ["404"]
        path = f"{dirname(__file__)}/locale/{lang}/no_brain.dialog"
        if isfile(path):
            with open(path) as f:
                lines = [l for l in f.read().split("\n")
                         if l.strip() and not l.startswith("#")]
        return random.choice(lines)


if __name__ == "__main__":
    bot = FailureSolver()
    print(bot.get_spoken_answer("hello!"))
    print(bot.spoken_answer("Olá", {"lang": "pt-pt"}))