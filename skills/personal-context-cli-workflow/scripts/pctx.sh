#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="${PCTX_PROJECT_ROOT:-$PWD}"

if [[ ! -f "${PROJECT_ROOT}/pyproject.toml" ]] || [[ ! -d "${PROJECT_ROOT}/src/personal_context_cli" ]]; then
  echo "Could not locate Personal Context CLI project at: ${PROJECT_ROOT}" >&2
  echo "Set PCTX_PROJECT_ROOT or run this script from project root." >&2
  exit 1
fi

PYTHON_BIN="${PROJECT_ROOT}/.venv/bin/python"
if [[ ! -x "${PYTHON_BIN}" ]]; then
  echo "Missing virtualenv Python: ${PYTHON_BIN}" >&2
  echo "Create it with: python3 -m venv .venv" >&2
  exit 1
fi

export PYTHONPATH="${PROJECT_ROOT}/src${PYTHONPATH:+:${PYTHONPATH}}"
exec "${PYTHON_BIN}" -m personal_context_cli "$@"
