# # chat/consumers.py
# import json
# import aiohttp
# from channels.generic.websocket import AsyncWebsocketConsumer
# from .models import ChatMessage
# from django.utils.timezone import now

# N8N_WEBHOOK_URL = "https://ahra2004.app.n8n.cloud/webhook/9a43b32a-0188-42e8-ad53-4788eb4af36d/chat"

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.session_id = self.scope["query_string"].decode("utf-8").split("session_id=")[-1]
#         await self.accept()

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         message = data.get("message")

#         # Save user message
#         ChatMessage.objects.create(
#             session_id=self.session_id,
#             sender="user",
#             message=message,
#             timestamp=now()
#         )

#         # Send to n8n webhook
#         async with aiohttp.ClientSession() as session:
#             async with session.post(N8N_WEBHOOK_URL, json={
#                 "sessionId": self.session_id,
#                 "action": "sendMessage",
#                 "chatInput": message
#             }) as resp:
#                 result = await resp.json()
        
#         reply = result[0]["output"]

#         # Save bot reply
#         ChatMessage.objects.create(
#             session_id=self.session_id,
#             sender="bot",
#             message=reply,
#             timestamp=now()
#         )

#         # Send to frontend
#         await self.send(json.dumps({
#             "message": reply
#         }))
# chat/consumers.py

# chat/consumers.py

# import json
# import aiohttp
# from channels.generic.websocket import AsyncWebsocketConsumer
# from .models import ChatMessage
# from django.utils.timezone import now
# from asgiref.sync import sync_to_async

# N8N_WEBHOOK_URL = "https://ahra2004.app.n8n.cloud/webhook/9a43b32a-0188-42e8-ad53-4788eb4af36d/chat"

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.session_id = self.scope["query_string"].decode("utf-8").split("session_id=")[-1]
#         await self.accept()

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         message = data.get("message")

#         # Save user message async
#         await self.save_message(self.session_id, "user", message)

#         # Default reply
#         reply = "⚠️ حدث خطأ أثناء التواصل مع النظام الذكي."

#         # Send to n8n webhook
#         try:
#             async with aiohttp.ClientSession() as session:
#                 async with session.post(N8N_WEBHOOK_URL, json={
#                     "sessionId": self.session_id,
#                     "action": "sendMessage",
#                     "chatInput": message
#                 }) as resp:
#                     if resp.status == 200:
#                         result = await resp.json()
#                         print("RECEIVED FROM N8N:", result)  # أضف هذا السطر

#                         if isinstance(result, list) and result and "output" in result[0]:
#                             # reply = result[0]["output"]
#                             reply = result["output"]

#                         else:
#                             reply = "⚠️ رد غير متوقع من النظام الذكي."
#                     else:
#                         reply = f"⚠️ فشل في الاتصال بالنظام، الكود: {resp.status}"
#         except Exception as e:
#             print("Webhook Error:", str(e))

#         # Save bot reply async
#         await self.save_message(self.session_id, "bot", reply)

#         # Send to frontend
#         await self.send(json.dumps({
#             "message": reply
#         }))

#     @sync_to_async
#     def save_message(self, session_id, sender, message):
#         ChatMessage.objects.create(
#             session_id=session_id,
#             sender=sender,
#             message=message,
#             timestamp=now()
#         )
import json
import aiohttp
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatMessage
from django.utils.timezone import now
from asgiref.sync import sync_to_async
N8N_WEBHOOK_URL = "https://n8n.thepost.digital/webhook/91822092-5356-41ac-bb03-58100cffd404/chat"

# N8N_WEBHOOK_URL = "https://ahra2004.app.n8n.cloud/webhook/9a43b32a-0188-42e8-ad53-4788eb4af36d/chat"
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.session_id = self.scope["query_string"].decode("utf-8").split("session_id=")[-1]
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message")

        # حفظ رسالة المستخدم
        await self.save_message(self.session_id, "user", message)

        reply = "⚠️ حدث خطأ أثناء التواصل مع النظام الذكي."

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(N8N_WEBHOOK_URL, json={
                    "sessionId": self.session_id,
                    "action": "sendMessage",
                    "chatInput": message
                }) as resp:
                    if resp.status == 200:
                        result = await resp.json()
                        print("RECEIVED FROM N8N:", result)

                        # هنا بنفحص نوع الاستجابة
                        if isinstance(result, dict) and "output" in result:
                            reply = result["output"]
                        elif isinstance(result, list) and len(result) > 0 and "output" in result[0]:
                            reply = result[0]["output"]
                        else:
                            reply = "⚠️ رد غير متوقع من النظام الذكي."
                    else:
                        reply = f"⚠️ فشل في الاتصال بالنظام، الكود: {resp.status}"
        except Exception as e:
            print("Webhook Error:", str(e))
            reply = "⚠️ تعذر الاتصال بالنظام الذكي."

        # حفظ رد البوت
        await self.save_message(self.session_id, "bot", reply)

        # إرسال الرد للفرونت
        await self.send(json.dumps({
            "message": reply
        }))

    @sync_to_async
    def save_message(self, session_id, sender, message):
        ChatMessage.objects.create(
            session_id=session_id,
            sender=sender,
            message=message,
            timestamp=now()
        )
