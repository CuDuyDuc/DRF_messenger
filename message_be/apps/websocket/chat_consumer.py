import json
import logging
from django.contrib.auth import get_user_model

from .base_consumer import BaseConsumer
from asgiref.sync import sync_to_async
from message_be.apps.models_container import Message

logger = logging.getLogger("__name__")
User = get_user_model()

class ChatConsumer(BaseConsumer):
    room_group_name = str

    async def join_group(self):
        self.room_group_name = f'chat_{self.user.id}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        try:
            data = json.loads(text_data)
            print("Data received from FE:", data)
            await self.process_message(data)
        except Exception as e:
            logger.exception("Error in receive: %s", e)

    async def process_message(self, data):
        message_content = data['message']
        sender = self.user
        recipient_id = data['recipient']

        recipient = await sync_to_async(User.objects.filter(id=recipient_id).first)()
        if recipient:
            message = Message(
                sender=sender,
                recipient=recipient,
                message_content=message_content
            )
            await sync_to_async(message.save)()

            response = {
                'sender': str(sender),
                'recipient': str(recipient),
                'message': message_content,
            }

            await self.channel_layer.group_send(
                f"chat_{recipient.id}",
                {
                    'type': 'chat_message',
                    'message': response
                }
            )

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))
