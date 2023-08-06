from __future__ import annotations

import logging
from contextlib import suppress
from dataclasses import dataclass
from typing import TYPE_CHECKING

from better_translation.integrations.django.models import BaseMessage
from better_translation.storage import (
    BaseStorage,
    StorageMessage,
    StorageTranslation,
)

if TYPE_CHECKING:
    from pathlib import Path


logger = logging.getLogger(__name__)


@dataclass(slots=True)
class DjangoStorage(BaseStorage):
    message_model: type[BaseMessage] = BaseMessage

    def __post_init__(self) -> None:
        if self.message_model is BaseMessage:
            msg = "`message_model` is required"
            raise ValueError(msg)

    async def load(self) -> None:
        """Load translations from the storage to the memory."""
        logger.info("Loading messages from the database...")

        messages = self.message_model.objects.all().prefetch_related(
            "translations",
        )
        async for message in messages:
            translations = message.translations.all()
            if not translations:
                logger.warning(
                    "Message '%s' has no translations",
                    message,
                )
            else:
                logger.debug(
                    "Message '%s' has '%s' translations",
                    message,
                    len(translations),
                )

            self.storage[message.id] = StorageMessage(
                id=message.id,
                default=message.default,
                default_plural=message.default_plural,
                context=message.context,
                has_plural=message.has_plural,
                translations={
                    translation.locale: StorageTranslation(
                        singular=translation.singular,
                        plural=translation.singular,
                    )
                    for translation in translations
                },
            )

        self.is_loaded = True

        logger.info("Messages loaded successfully")

    async def update_messages(
        self,
        directory_path: Path,
    ) -> None:
        if not self.is_loaded:
            logger.info("Cannot update messages, storage is not loaded...")
            await self.load()

        logger.info("Updating messages from the directory...")

        new_messages: set[BaseMessage] = set()
        unused_messages = set(self.storage)

        messages = self._extract_messages(directory_path)
        for message in messages:
            if message.id in self.storage:
                with suppress(KeyError):
                    unused_messages.remove(message.id)

                saved_message = self.storage[message.id]
                if (
                    message.updatable_attributes
                    != saved_message.updatable_attributes
                ):
                    logger.debug(
                        "Message '%s' has different attributes, updating...",
                        message,
                    )
                    self.storage[message.id] = message

                continue

            logger.debug(
                "Message '%s' is new, adding to the database...",
                message,
            )
            new_messages.add(self._init_message_model(message))
            self.storage[message.id] = message

        await self.message_model.objects.abulk_create(new_messages)
        updated_messages_count: int = (
            # pyright: reportGeneralTypeIssues=false
            await self.message_model.objects.abulk_update(
                (
                    self._init_message_model(message)
                    for message in self.storage.values()
                ),
                fields=(
                    "has_plural",
                    "context",
                ),
            )
        )
        await self.message_model.objects.filter(
            id__in=unused_messages,
        ).aupdate(is_used=False)

        logger.info(
            "Updated %s messages, created %s messages, found %s unused messages",
            updated_messages_count,
            len(new_messages),
            len(unused_messages),
        )

    def _init_message_model(
        self,
        storage_message: StorageMessage,
    ) -> BaseMessage:
        return self.message_model(
            id=storage_message.id,
            default=storage_message.default,
            default_plural=storage_message.default_plural,
            context=storage_message.context,
            has_plural=storage_message.has_plural,
        )
