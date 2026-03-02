from __future__ import annotations

import pytest

from personal_context_cli.cli import build_parser


def test_ask_accepts_question_without_type_flag() -> None:
    parser = build_parser()
    args = parser.parse_args(
        [
            "ask",
            "hello",
            "--data-file",
            "profile.enc",
        ]
    )
    assert args.command == "ask"
    assert args.question == "hello"


def test_ask_accepts_type_flag() -> None:
    parser = build_parser()
    args = parser.parse_args(
        [
            "ask",
            "hello",
            "--type",
            "finance",
            "--data-file",
            "profile.enc",
        ]
    )
    assert args.command == "ask"
    assert args.question == "hello"
    assert args.type == "finance"
