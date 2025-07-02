# import requests
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import ChatMessage, UserSubmission
# from .serializers import ChatMessageSerializer, UserSubmissionSerializer

# N8N_WEBHOOK_URL = "https://ahmed0202.app.n8n.cloud/webhook/3a8ab3ce-625e-4649-aa3c-9fa2b734a174/chat"

# class SendMessageView(APIView):
#     def post(self, request):
#         session_id = request.data.get("session_id")
#         user_message = request.data.get("message")

#         if not user_message or not session_id:
#             return Response({"error": "Missing message or session_id"}, status=400)

#         # Save user's message
#         ChatMessage.objects.create(
#             session_id=session_id,
#             message=user_message,
#             sender="user"
#         )

#         # Send to n8n webhook
#         try:
#             res = requests.post(N8N_WEBHOOK_URL, json={
#                 "sessionId": session_id,
#                 "action": "sendMessage",
#                 "chatInput": user_message
#             })

#             reply = res.json()[0]["output"]

#             # Save bot's message
#             ChatMessage.objects.create(
#                 session_id=session_id,
#                 message=reply,
#                 sender="bot"
#             )

#             return Response({"reply": reply})
#         # except Exception as e:
#         #     return Response({"error": str(e)}, status=500)
#         except Exception as e:
#             return Response({"error": str(e)}, status=500)        

# class SubmitFormView(APIView):
#     def post(self, request):
#         serializer = UserSubmissionSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"status": "saved"})
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# from rest_framework.generics import ListAPIView
# from .models import ChatMessage
# from .serializers import ChatMessageSerializer
# from rest_framework.permissions import AllowAny
# from rest_framework.filters import OrderingFilter
# from django_filters.rest_framework import DjangoFilterBackend

# class ChatHistoryView(ListAPIView):
#     serializer_class = ChatMessageSerializer
#     permission_classes = [AllowAny]
#     filter_backends = [DjangoFilterBackend, OrderingFilter]
#     filterset_fields = ['session_id']
#     ordering_fields = ['timestamp']
#     ordering = ['timestamp']

#     def get_queryset(self):
#         return ChatMessage.objects.all()
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ChatMessage, UserSubmission
from .serializers import ChatMessageSerializer, UserSubmissionSerializer

N8N_WEBHOOK_URL = "https://ahra2004.app.n8n.cloud/webhook/9a43b32a-0188-42e8-ad53-4788eb4af36d/chat"


class SendMessageView(APIView):
    def post(self, request):
        session_id = request.data.get("session_id")
        user_message = request.data.get("message")

        if not user_message or not session_id:
            return Response(
                {"error": "Missing 'message' or 'session_id'"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Save user's message
        ChatMessage.objects.create(
            session_id=session_id,
            message=user_message,
            sender="user"
        )

        try:
            # Send to n8n webhook
            res = requests.post(N8N_WEBHOOK_URL, json={
                "sessionId": session_id,
                "action": "sendMessage",
                "chatInput": user_message
            })

            res.raise_for_status()  # ⬅️ مهم جدًا عشان يطلعلك لو فيه مشكلة HTTP

            # result = res.json()

            # تحقق إن الرد من n8n على الشكل المتوقع
            # if not isinstance(result, list) or "output" not in result[0]:
            #     return Response(
            #         {"error": "Unexpected response format from n8n", "raw": result},
            #         status=status.HTTP_502_BAD_GATEWAY
            #     )

            # reply = result[0]["output"]
            result = res.json()

            # دعم النوعين: dict أو list
            if isinstance(result, list) and "output" in result[0]:
                reply = result[0]["output"]
            elif isinstance(result, dict) and "output" in result:
                reply = result["output"]
            else:
                return Response(
                    {"error": "Unexpected response structure from n8n", "raw": result},
                    status=status.HTTP_502_BAD_GATEWAY
                )

            # Save bot's message
            ChatMessage.objects.create(
                session_id=session_id,
                message=reply,
                sender="bot"
            )

            return Response({"reply": reply})

        except requests.exceptions.RequestException as req_err:
            return Response(
                {"error": f"Request error to n8n: {str(req_err)}"},
                status=status.HTTP_502_BAD_GATEWAY
            )

        except (KeyError, IndexError, ValueError) as json_err:
            return Response(
                {"error": f"Invalid response from n8n: {str(json_err)}"},
                status=status.HTTP_502_BAD_GATEWAY
            )

        except Exception as e:
            return Response(
                {"error": f"General error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SubmitFormView(APIView):
    def post(self, request):
        serializer = UserSubmissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "saved"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.generics import ListAPIView
from .models import ChatMessage
from .serializers import ChatMessageSerializer
from rest_framework.permissions import AllowAny
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


class ChatHistoryView(ListAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['session_id']
    ordering_fields = ['timestamp']
    ordering = ['timestamp']

    def get_queryset(self):
        return ChatMessage.objects.all()
