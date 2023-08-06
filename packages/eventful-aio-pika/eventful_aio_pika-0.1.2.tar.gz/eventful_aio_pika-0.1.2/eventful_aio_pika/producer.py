import json
import logging
from typing import Any

from aio_pika import Message
from aio_pika.abc import (
    AbstractChannel,
    AbstractConnection,
    AbstractExchange,
    DeliveryMode,
)


class RabbitProducer:
    def __init__(self, queue: str) -> None:
        self.exchange: AbstractExchange | None = None
        self.queue: str = queue

    async def connect(self, connection: AbstractConnection) -> None:
        channel: AbstractChannel = await connection.channel()
        self.exchange = channel.default_exchange
        await channel.declare_queue(self.queue)

    async def send_event(self, data: Any, event_name: str | None = None) -> None:
        if self.exchange is None:
            raise RuntimeError("Client is not connected")
        message = Message(
            body=json.dumps(data).encode("utf-8"),
            headers={"event_name": event_name},
            delivery_mode=DeliveryMode.PERSISTENT,
        )
        await self.exchange.publish(message=message, routing_key=self.queue)
        logging.info(
            f"Sending event '{event_name}'",
            extra={"outgoing_message": message},
        )
