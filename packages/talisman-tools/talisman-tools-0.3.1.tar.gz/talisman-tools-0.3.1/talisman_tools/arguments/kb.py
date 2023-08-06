from argparse import ArgumentParser, Namespace

from talisman_tools.plugin import KBPlugins
from tp_interfaces.helpers.io import read_json
from tp_interfaces.knowledge_base.manager import KBManager


def get_kb_factory(parser: ArgumentParser):
    parser.add_argument('-kb_config_path', metavar='<kb config path>')

    def set_kb(args: Namespace) -> None:
        if args.kb_config_path is None:
            return

        config = read_json(args.kb_config_path)
        kb = KBPlugins.plugins[config.get("plugin")]().from_config(config.get('config', {}))
        KBManager().knowledge_base = kb

    return set_kb
