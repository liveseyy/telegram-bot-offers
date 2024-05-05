import random
import pika

from django.conf import settings


class BaseSync:
    """
    Базовый класс для работы с RabbitMQ.
    Устанавливается подключение, создаются queue и exchange, используемые в приложении.
    """

    connection_mq = None
    mq_channel = None

    BOT_EXCHANGE = "bot"
    BOT__SEND_OFFERS_QUEUE = "bot__send_offers_to_user"
    BOT__SYNC_WATCHERS_WITH_OFFERS_QUEUE = "bot__sync_watchers_with_offers"

    def connect_mq(self, heartbeat=90):
        parameters = []
        credentials = pika.PlainCredentials(
            settings.RABBITMQ["USER"], settings.RABBITMQ["PASSWORD"]
        )
        for host in settings.RABBITMQ["HOSTS"].split(","):
            parameters.append(
                pika.ConnectionParameters(
                    host=host.strip(),
                    virtual_host=settings.RABBITMQ["VHOST"],
                    connection_attempts=5,
                    retry_delay=1,
                    credentials=credentials,
                    heartbeat=heartbeat,
                    blocked_connection_timeout=heartbeat,
                )
            )

        self.connection_mq = pika.BlockingConnection(random.choice(parameters))
        self.mq_channel = self.connection_mq.channel()
        self.mq_channel.exchange_declare(
            exchange=self.BOT_EXCHANGE, durable=True, auto_delete=False
        )

        self.mq_channel.queue_declare(queue=self.BOT__SEND_OFFERS_QUEUE, durable=True)
        self.mq_channel.queue_bind(self.BOT__SEND_OFFERS_QUEUE, self.BOT_EXCHANGE)

        self.mq_channel.queue_declare(queue=self.BOT__SYNC_WATCHERS_WITH_OFFERS_QUEUE, durable=True)
        self.mq_channel.queue_bind(self.BOT__SYNC_WATCHERS_WITH_OFFERS_QUEUE, self.BOT_EXCHANGE)
