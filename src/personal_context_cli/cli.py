import argparse
import json
from pathlib import Path

from .config import DEFAULT_PROFILE_PAYLOAD
from .context_selector import select_context
from .llm_adapter import generate_answer
from .services import (
    add_family_member,
    get_owner_profile,
    get_preferences,
    list_family_members,
    remove_family_member,
    set_owner_profile,
    set_preferences,
    update_family_member,
)
from .store import EncryptedStore


def _add_data_password_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--data-file", required=True)
    parser.add_argument("--password", required=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="personal-context")
    subcommands = parser.add_subparsers(dest="command")

    init_parser = subcommands.add_parser("init")
    _add_data_password_args(init_parser)

    ask_parser = subcommands.add_parser("ask")
    ask_parser.add_argument("question")
    ask_parser.add_argument("--type")
    ask_parser.add_argument(
        "--provider",
        choices=["auto", "codex", "claude", "api"],
        default="auto",
    )
    ask_parser.add_argument(
        "--relay-timeout-seconds",
        type=int,
        default=20,
        help="Timeout for codex/claude relay providers in seconds.",
    )
    ask_parser.add_argument(
        "--relay-retries",
        type=int,
        default=0,
        help="Retry count for relay timeout failures.",
    )
    _add_data_password_args(ask_parser)

    context_parser = subcommands.add_parser("context")
    context_sub = context_parser.add_subparsers(dest="context_command")
    context_preview = context_sub.add_parser("preview")
    context_preview.add_argument("question")
    context_preview.add_argument("--type")
    _add_data_password_args(context_preview)

    profile_parser = subcommands.add_parser("profile")
    profile_sub = profile_parser.add_subparsers(dest="profile_command")
    profile_set = profile_sub.add_parser("set")
    _add_data_password_args(profile_set)
    profile_set.add_argument("--age", type=int)
    profile_set.add_argument("--industry")
    profile_set.add_argument("--income-range")

    profile_get = profile_sub.add_parser("get")
    _add_data_password_args(profile_get)

    prefs_parser = subcommands.add_parser("prefs")
    prefs_sub = prefs_parser.add_subparsers(dest="prefs_command")
    prefs_set = prefs_sub.add_parser("set")
    _add_data_password_args(prefs_set)
    prefs_set.add_argument("--response-style")
    prefs_set.add_argument("--strategy-style")
    prefs_set.add_argument("--locale-bias")

    prefs_get = prefs_sub.add_parser("get")
    _add_data_password_args(prefs_get)

    family_parser = subcommands.add_parser("family")
    family_sub = family_parser.add_subparsers(dest="family_command")
    family_add = family_sub.add_parser("add")
    _add_data_password_args(family_add)
    family_add.add_argument("--relation", required=True)
    family_add.add_argument("--age-band")
    family_add.add_argument("--occupation-or-school")

    family_list = family_sub.add_parser("list")
    _add_data_password_args(family_list)

    family_update = family_sub.add_parser("update")
    _add_data_password_args(family_update)
    family_update.add_argument("--id", required=True)
    family_update.add_argument("--relation")
    family_update.add_argument("--age-band")
    family_update.add_argument("--occupation-or-school")

    family_remove = family_sub.add_parser("remove")
    _add_data_password_args(family_remove)
    family_remove.add_argument("--id", required=True)

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
    if args.command == "profile":
        if args.profile_command == "set":
            set_owner_profile(
                data_file=args.data_file,
                password=args.password,
                age=args.age,
                industry=args.industry,
                income_range=args.income_range,
            )
            return 0
        if args.profile_command == "get":
            profile = get_owner_profile(args.data_file, args.password)
            print(json.dumps(profile, ensure_ascii=False))
            return 0
    if args.command == "prefs":
        if args.prefs_command == "set":
            set_preferences(
                data_file=args.data_file,
                password=args.password,
                response_style=args.response_style,
                strategy_style=args.strategy_style,
                locale_bias=args.locale_bias,
            )
            return 0
        if args.prefs_command == "get":
            prefs = get_preferences(args.data_file, args.password)
            print(json.dumps(prefs, ensure_ascii=False))
            return 0
    if args.command == "family":
        if args.family_command == "add":
            member = add_family_member(
                data_file=args.data_file,
                password=args.password,
                relation=args.relation,
                age_band=args.age_band,
                occupation_or_school=args.occupation_or_school,
            )
            print(json.dumps(member, ensure_ascii=False))
            return 0
        if args.family_command == "list":
            members = list_family_members(args.data_file, args.password)
            print(json.dumps(members, ensure_ascii=False))
            return 0
        if args.family_command == "update":
            updated = update_family_member(
                data_file=args.data_file,
                password=args.password,
                member_id=args.id,
                relation=args.relation,
                age_band=args.age_band,
                occupation_or_school=args.occupation_or_school,
            )
            return 0 if updated else 1
        if args.family_command == "remove":
            removed = remove_family_member(
                data_file=args.data_file,
                password=args.password,
                member_id=args.id,
            )
            return 0 if removed else 1
    if args.command == "context":
        if args.context_command == "preview":
            payload = EncryptedStore(Path(args.data_file)).load(args.password)
            context = select_context(args.question, args.type, payload)
            print(json.dumps(context, ensure_ascii=False))
            return 0
    if args.command == "ask":
        payload = EncryptedStore(Path(args.data_file)).load(args.password)
        context = select_context(args.question, args.type, payload)
        answer = generate_answer(
            args.question,
            context,
            provider=args.provider,
            relay_timeout_seconds=args.relay_timeout_seconds,
            relay_retries=args.relay_retries,
        )
        print(answer)
        return 0

    return 0
