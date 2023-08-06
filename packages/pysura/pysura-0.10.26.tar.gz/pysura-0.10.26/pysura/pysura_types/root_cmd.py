# INSTRUCTIONS FOR GPT4

# Rewrite the CMD loop to be more succinct and use prompt_toolkit features for history

from cmd import Cmd
from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.completion import WordCompleter
import inspect
import logging
import sys

root = logging.getLogger()
root.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(fmt="%(asctime)s %(filename)-25s %(levelname)-5s %(message)s",
                              datefmt="%Y-%m-%d %I:%H:%M")
handler.setFormatter(formatter)
root.addHandler(handler)


class RootCmd(Cmd):

    def setup_logging(self):
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        root_handler = logging.StreamHandler(sys.stdout)
        root_handler.setLevel(logging.DEBUG)
        root_formatter = logging.Formatter(fmt="%(asctime)s %(levelname)-5s %(message)s",
                                           datefmt="%Y-%m-%d %I:%H:%M")
        root_handler.setFormatter(root_formatter)
        root_logger.addHandler(root_handler)
        self.root = root_logger

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prompt = "root> "
        self.completer = WordCompleter([
            *[i[0][3:] for i in inspect.getmembers(self, predicate=inspect.isfunction) if
              i[0].startswith("do_")],
            *[i[0][3:] for i in inspect.getmembers(self, predicate=inspect.ismethod) if
              i[0].startswith("do_")]
        ])
        self.root = None
        self.setup_logging()

    def cmdloop(self, intro=None):
        self.preloop()
        history = InMemoryHistory()

        try:
            if intro is not None:
                self.intro = intro
            if self.intro:
                self.stdout.write(str(self.intro) + "\n")
            stop = None
            while not stop:
                try:
                    line = prompt(
                        self.prompt,
                        completer=self.completer,
                        history=history
                    )
                except EOFError:
                    line = 'EOF'
                line = self.precmd(line)
                stop = self.onecmd(line)
                stop = self.postcmd(stop, line)
            self.postloop()
        finally:
            pass

    @staticmethod
    def log(log_str: str, level=logging.INFO):
        logging.log(level, log_str)

    @staticmethod
    def collect(collect_str: str, completer=None):
        if isinstance(completer, list):
            completer = WordCompleter(completer)
        else:
            completer = None
        try:
            input_str = prompt(
                f"{collect_str}",
                completer=completer
            )
            if len(input_str.strip()) == 0:
                return RootCmd.collect(collect_str, completer)
            elif input_str.strip() in ["exit", "quit"]:
                RootCmd.log("\nExiting...")
                exit(0)
            else:
                return input_str
        except KeyboardInterrupt:
            RootCmd.log("\nKeyboardInterrupt. Exiting...")
            exit(1)
