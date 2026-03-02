import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="personal-context")
    subcommands = parser.add_subparsers(dest="command")
    subcommands.add_parser("init")
    subcommands.add_parser("ask")
    return parser


def main() -> int:
    parser = build_parser()
    parser.parse_args()
    return 0
