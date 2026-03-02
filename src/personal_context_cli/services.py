from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from .models import FamilyMember, OwnerProfile, Preferences
from .store import EncryptedStore


def _load_payload(data_file: str, password: str) -> dict:
    return EncryptedStore(Path(data_file)).load(password)


def _save_payload(data_file: str, password: str, payload: dict) -> None:
    EncryptedStore(Path(data_file)).save(payload, password)


def set_owner_profile(
    data_file: str,
    password: str,
    age: int | None = None,
    industry: str | None = None,
    income_range: str | None = None,
) -> None:
    payload = _load_payload(data_file, password)
    owner = dict(payload.get("owner_profile", {}))
    if age is not None:
        owner["age"] = age
    if industry is not None:
        owner["industry"] = industry
    if income_range is not None:
        owner["income_range"] = income_range

    required = {"age", "industry", "income_range"}
    if required.issubset(owner):
        OwnerProfile(**owner)

    payload["owner_profile"] = owner
    _save_payload(data_file, password, payload)


def get_owner_profile(data_file: str, password: str) -> dict:
    payload = _load_payload(data_file, password)
    return payload.get("owner_profile", {})


def set_preferences(
    data_file: str,
    password: str,
    response_style: str | None = None,
    strategy_style: str | None = None,
    locale_bias: str | None = None,
) -> None:
    payload = _load_payload(data_file, password)
    prefs = dict(payload.get("preferences", {}))
    if response_style is not None:
        prefs["response_style"] = response_style
    if strategy_style is not None:
        prefs["strategy_style"] = strategy_style
    if locale_bias is not None:
        prefs["locale_bias"] = locale_bias
    Preferences(**prefs)
    payload["preferences"] = prefs
    _save_payload(data_file, password, payload)


def get_preferences(data_file: str, password: str) -> dict:
    payload = _load_payload(data_file, password)
    return payload.get("preferences", {})


def add_family_member(
    data_file: str,
    password: str,
    relation: str,
    age_band: str | None = None,
    occupation_or_school: str | None = None,
) -> dict:
    payload = _load_payload(data_file, password)
    members = list(payload.get("family_members", []))
    member = FamilyMember(
        id=str(uuid4()),
        relation=relation,
        age_band=age_band,
        occupation_or_school=occupation_or_school,
    )
    members.append(member.model_dump())
    payload["family_members"] = members
    _save_payload(data_file, password, payload)
    return member.model_dump()


def list_family_members(data_file: str, password: str) -> list[dict]:
    payload = _load_payload(data_file, password)
    return payload.get("family_members", [])


def update_family_member(
    data_file: str,
    password: str,
    member_id: str,
    relation: str | None = None,
    age_band: str | None = None,
    occupation_or_school: str | None = None,
) -> bool:
    payload = _load_payload(data_file, password)
    members = list(payload.get("family_members", []))
    updated = False
    for item in members:
        if item.get("id") == member_id:
            if relation is not None:
                item["relation"] = relation
            if age_band is not None:
                item["age_band"] = age_band
            if occupation_or_school is not None:
                item["occupation_or_school"] = occupation_or_school
            FamilyMember(**item)
            updated = True
            break

    if updated:
        payload["family_members"] = members
        _save_payload(data_file, password, payload)
    return updated


def remove_family_member(data_file: str, password: str, member_id: str) -> bool:
    payload = _load_payload(data_file, password)
    members = list(payload.get("family_members", []))
    filtered = [member for member in members if member.get("id") != member_id]
    changed = len(filtered) != len(members)
    if changed:
        payload["family_members"] = filtered
        _save_payload(data_file, password, payload)
    return changed
