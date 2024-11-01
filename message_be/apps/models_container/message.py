from django.db import models
from django.contrib.auth import get_user_model
from cryptography.fernet import Fernet
import os

User = get_user_model()

KEY = os.environ.get("FERNET_KEY") or Fernet.generate_key()
cipher = Fernet(KEY)

class Message(models.Model):
    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name="received_messages", on_delete=models.CASCADE)
    message_content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def encrypt_message(message):
        return cipher.encrypt(message.encode('utf-8'))

    def decrypt_message(self):
        encrypted_content = (
            self.message_content.encode('utf-8') if isinstance(self.message_content, str) else self.message_content
        )
        return cipher.decrypt(encrypted_content).decode('utf-8')

    def save(self, *args, **kwargs):
        if isinstance(self.message_content, str):
            self.message_content = self.encrypt_message(self.message_content)
        super().save(*args, **kwargs)
