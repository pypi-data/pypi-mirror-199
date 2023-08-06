from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from better_translation.extractor import extract_from_dir

if TYPE_CHECKING:
    from collections.abc import Iterable, Mapping
    from pathlib import Path

    from better_translation.types import (
        Locale,
        MessageID,
        TranslatedText,
    )

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class StorageMessage:
    id: MessageID
    default: TranslatedText
    default_plural: TranslatedText
    context: str
    has_plural: bool
    translations: Mapping[Locale, StorageTranslation]

    @property
    def updatable_attributes(self) -> tuple[Any, ...]:
        return (
            self.context,
            self.has_plural,
        )


@dataclass(slots=True)
class StorageTranslation:
    singular: TranslatedText
    plural: TranslatedText


class IStorage(ABC):
    @abstractmethod
    def get_message(self, message_id: MessageID) -> StorageMessage | None:
        """Get a message from the storage."""

    @abstractmethod
    async def load(self) -> None:
        """Load translations from the storage to the memory."""

    @abstractmethod
    async def update_messages(
        self,
        directory_path: Path,
    ) -> None:
        """Update untranslated messages from the directory in the storage."""


@dataclass(slots=True)
class BaseStorage(IStorage, ABC):
    storage: dict[MessageID, StorageMessage] = field(
        default_factory=dict,
        init=False,
    )
    is_loaded: bool = field(default=False, init=False)

    def get_message(self, message_id: MessageID) -> StorageMessage | None:
        if not self.is_loaded:
            msg = "Cannot get translation, storage is not loaded..."
            raise ValueError(msg)

        return self.storage.get(message_id)

    @staticmethod
    def _extract_messages(directory_path: Path) -> Iterable[StorageMessage]:
        for message in extract_from_dir(directory_path):
            yield StorageMessage(
                id=message.id,
                default=message.default or message.id,
                default_plural=message.default_plural or message.id,
                context=str(message.context) if message.context else "",
                has_plural="n" in message.extra,
                translations={},
            )
