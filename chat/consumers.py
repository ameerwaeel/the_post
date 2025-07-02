# chat/consumers.py
import json
import aiohttp
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatMessage
from django.utils.timezone import now

N8N_WEBHOOK_URL = "https://ahra2004.app.n8n.cloud/webhook/9a43b32a-0188-42e8-ad53-4788eb4af36d/chat"

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.session_id = self.scope["query_string"].decode("utf-8").split("session_id=")[-1]
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message")

        # Save user message
        ChatMessage.objects.create(
            session_id=self.session_id,
            sender="user",
            message=message,
            timestamp=now()
        )

        # Send to n8n webhook
        async with aiohttp.ClientSession() as session:
            async with session.post(N8N_WEBHOOK_URL, json={
                "sessionId": self.session_id,
                "action": "sendMessage",
                "chatInput": message
            }) as resp:
                result = await resp.json()
        
        reply = result[0]["output"]

        # Save bot reply
        ChatMessage.objects.create(
            session_id=self.session_id,
            sender="bot",
            message=reply,
            timestamp=now()
        )

        # Send to frontend
        await self.send(json.dumps({
            "message": reply
        }))
