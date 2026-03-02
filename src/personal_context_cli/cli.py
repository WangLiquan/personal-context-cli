import argparse
from pathlib import Path

from .config import DEFAULT_PROFILE_PAYLOAD
from .store import EncryptedStore

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="personal-context")
    subcommands = parser.add_subparsers(dest="command")
    init_parser = subcommands.add_parser("init")
    init_parser.add_argument("--data-file", required=True)
    init_parser.add_argument("--password", required=True)
    subcommands.add_parser("ask")
    return parser


def _handle_init(data_file: str, password: str) -> int:
    store = EncryptedStore(Path(data_file))
    store.save(DEFAULT_PROFILE_PAYLOAD, password)
    return 0


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "init":
        return _handle_init(args.data_file, args.password)

    return 0
