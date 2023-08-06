from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Callable

from talisman_tools.arguments.kb import get_kb_factory
from talisman_tools.plugin import ReaderPlugins


def configure_kb_parser(parser: ArgumentParser) -> None:
    kb_factory = get_kb_factory(parser)

    parser.add_argument('reader', type=str, metavar='<reader>', choices=ReaderPlugins.flattened.keys())
    parser.add_argument('-mapping', '--concepts_mapping_docs', action='append', type=str,
                        metavar='<path to jsonl serialized concepts> <path to types mapping config> <path to gold docs with concepts>',
                        help='set <path to types mapping config> to "_" to ignore mapping')
    parser.add_argument('-conflict_resolution_order', type=Path, metavar='<json types list file path>')
    parser.add_argument('-concept_name_wo_id', action="store_true", help='<Use to create concept with name without id>')

    def get_action() -> Callable[[Namespace], None]:
        def action(args: Namespace) -> None:
            from .action import action
            kb_factory(args)
            return action(args)

        return action

    parser.set_defaults(action=get_action)
