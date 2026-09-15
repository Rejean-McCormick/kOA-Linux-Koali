"""Registered bounded worker identities for the implemented worker modules."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from types import MappingProxyType
from typing import Mapping


class WorkerKind(StrEnum):
    THUMBNAIL = "thumbnail"
    PREVIEW = "preview"
    TEXT_EXTRACTION = "text_extraction"


@dataclass(frozen=True, slots=True)
class WorkerDescriptor:
    worker_kind: WorkerKind
    module: str
    deterministic: bool
    resource_governor_required: bool
    owns_authoritative_metadata: bool = False


WORKERS: Mapping[WorkerKind, WorkerDescriptor] = MappingProxyType(
    {
        WorkerKind.THUMBNAIL: WorkerDescriptor(
            WorkerKind.THUMBNAIL,
            "koa_mediatheque.workers.thumbnail_worker",
            True,
            True,
        ),
        WorkerKind.PREVIEW: WorkerDescriptor(
            WorkerKind.PREVIEW,
            "koa_mediatheque.workers.preview_worker",
            True,
            True,
        ),
        WorkerKind.TEXT_EXTRACTION: WorkerDescriptor(
            WorkerKind.TEXT_EXTRACTION,
            "koa_mediatheque.workers.text_extraction_worker",
            True,
            True,
        ),
    }
)


def get_worker_descriptor(kind: WorkerKind | str) -> WorkerDescriptor:
    """Return a registered descriptor without importing or starting a worker module."""
    return WORKERS[WorkerKind(kind)]


__all__ = ["WORKERS", "WorkerDescriptor", "WorkerKind", "get_worker_descriptor"]
