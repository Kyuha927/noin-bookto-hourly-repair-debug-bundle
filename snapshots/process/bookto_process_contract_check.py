#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "pydantic>=2.13,<3",
#     "typing-extensions>=4.12,<5",
#     "typer>=0.21,<1",
# ]
# ///

"""Fail-closed Bookto lane process identity checker."""

from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated

import typer
from pydantic import ValidationError
from typing_extensions import override

from bookto_process_contract_evaluator import evaluate_contract, evaluate_documents
from bookto_process_contract_models import ProcessContract, RuntimeSnapshot
from bookto_process_contract_runtime import (
    RuntimeCommandError,
    SnapshotFieldError,
    collect_snapshot,
)

__all__ = [
    "ContractIntegrityError",
    "evaluate_contract",
    "evaluate_documents",
    "read_verified_contract",
    "run_cli",
]


@dataclass(frozen=True, slots=True)
class ContractIntegrityError(Exception):
    contract_path: Path

    @override
    def __str__(self) -> str:
        return f"contract checksum mismatch: {self.contract_path}"


def read_verified_contract(contract_path: Path) -> str:
    """Read a contract only when its adjacent SHA-256 sidecar matches exactly."""
    document = contract_path.read_text(encoding="utf-8")
    checksum_path = contract_path.with_suffix(contract_path.suffix + ".sha256")
    parts = checksum_path.read_text(encoding="utf-8").split()
    digest = hashlib.sha256(document.encode()).hexdigest()
    valid = (
        len(parts) == 2
        and parts[0] == digest
        and Path(parts[1]).name == contract_path.name
    )
    if not valid:
        raise ContractIntegrityError(contract_path=contract_path)
    return document


def _atomic_write(path: Path, document: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    _ = temporary.write_text(document + "\n", encoding="utf-8")
    os.replace(temporary, path)


def run_cli(
    contract_path: Path,
    snapshot_path: Path | None,
    output_path: Path | None,
) -> int:
    """Run one checksum-bound read-only check and persist its exact report."""
    contract_document = read_verified_contract(contract_path)
    contract = ProcessContract.model_validate_json(contract_document)
    if snapshot_path is None:
        snapshot = collect_snapshot(contract)
        snapshot_document = snapshot.model_dump_json()
    else:
        snapshot_document = snapshot_path.read_text(encoding="utf-8")
        snapshot = RuntimeSnapshot.model_validate_json(snapshot_document)
    report = evaluate_contract(
        contract,
        snapshot,
        source_hashes=(
            hashlib.sha256(contract_document.encode()).hexdigest(),
            hashlib.sha256(snapshot_document.encode()).hexdigest(),
        ),
    )
    document = report.model_dump_json(indent=2)
    _atomic_write(output_path or contract.status_output_path, document)
    print(document, flush=True)
    return 0 if report.status == "PASS" else 2


def main(
    contract: Annotated[Path, typer.Option(exists=True, dir_okay=False)],
    snapshot: Annotated[Path | None, typer.Option(exists=True, dir_okay=False)] = None,
    output: Annotated[Path | None, typer.Option(dir_okay=False)] = None,
) -> None:
    """Check exact process identity; exit 2 for detected runtime drift."""
    try:
        returncode = run_cli(contract, snapshot, output)
    except (
        ContractIntegrityError,
        OSError,
        RuntimeCommandError,
        SnapshotFieldError,
        ValidationError,
    ) as error:
        error_document = (
            f'{{"schema_version":"bookto_process_report.v1",'
            f'"status":"ERROR","error_type":"{type(error).__name__}"}}'
        )
        print(error_document, flush=True)
        raise typer.Exit(code=3) from error
    if returncode:
        raise typer.Exit(code=returncode)


if __name__ == "__main__":
    typer.run(main)
