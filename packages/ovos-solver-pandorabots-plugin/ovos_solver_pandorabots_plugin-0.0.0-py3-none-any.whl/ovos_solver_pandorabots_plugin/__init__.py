from os import listdir, remove as remove_file
from os.path import dirname, isfile
from os.path import join, dirname

import all_the_chatbots
import os
import random
from datetime import date
from neon_solvers import AbstractSolver
from ovos_utils.log import LOG


class PandoraBotsSolver(AbstractSolver):
    bots = all_the_chatbots.bot_map()

    def __init__(self, config=None):
        super().__init__(name="PandoraBots", priority=97, config=config,
                         enable_cache=False, enable_tx=True)
        self.default_bot = self.config.get("bot", "professor")

    # officially exported Solver methods
    def get_spoken_answer(self, query, context=None):
        context = context or {}
        bot_name = context.get("bot") or self.default_bot
        if bot_name in self.bots:
            return self.bots[bot_name](query)
        for bot in self.bots.values():
            try:
                return bot(query)
            except:
                continue


if __name__ == "__main__":
    bot = PandoraBotsSolver()
    print(bot.get_spoken_answer("hello!"))
    print(bot.spoken_answer("Qual é a tua comida favorita?", {"lang": "pt-pt"}))
