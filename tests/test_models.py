import pytest
from pydantic import ValidationError

from personal_context_cli.models import OwnerProfile


def test_owner_profile_requires_valid_age() -> None:
    with pytest.raises(ValidationError):
        OwnerProfile(age=-1, industry="tech", income_range="30-50w")
