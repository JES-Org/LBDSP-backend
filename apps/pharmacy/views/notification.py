from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from apps.pharmacy.models.notifications import Notification
from apps.pharmacy.serializers.notification import NotificationSerializer

class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_role = request.user.role 
        notifications = Notification.objects.filter(notify=user_role,is_read=False).order_by('-created_at')
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class MarkNotificationAsReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, notification_id):
        try:
            notification = Notification.objects.get(id=notification_id)
            notification.is_read = True
            notification.save()
            return Response({"message": "Notification marked as read"}, status=status.HTTP_200_OK)
        except Notification.DoesNotExist:
            return Response({"error": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)
