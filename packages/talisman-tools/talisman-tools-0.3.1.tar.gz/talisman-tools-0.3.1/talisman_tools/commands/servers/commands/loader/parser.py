from argparse import ArgumentParser, Namespace
from typing import Callable

from fastapi import FastAPI

from talisman_tools.arguments.kb import get_kb_factory


def configure_loader_parser(parser: ArgumentParser) -> None:
    kb_factory = get_kb_factory(parser)

    def get_action() -> Callable[[Namespace], FastAPI]:
        def action_with_extra(args: Namespace) -> FastAPI:
            from .action import action
            kb_factory(args)
            return action(args)

        return action_with_extra

    parser.set_defaults(server_action=get_action)
