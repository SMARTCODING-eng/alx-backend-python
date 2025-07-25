from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import User, Conversation, Message
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows 
    users to be viewed or edited
    """
    queryset = User.objects.all().order_by('_date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ConversationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows conversations to be viewed,
    created, or updated.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [ permissions.IsAuthenticated]
    filters = {
        'search_fields': ['participants__username'],  # Assuming User model has a 'username' field
        'ordering_fields': ['created_at'],  }

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.request.user.conversations.all()
        return Conversation.objects.none()
    
    def create(self, request, *args, **kwargs):
        participant_ids = request.data.get('participant', [])
        if not participant_ids or not isinstance(participant_ids, list) or len(participant_ids) < 1:
            return Response(
                {"detail": "At least one participant is required to create a conversation."},
                status=status.HTTP_400_BAD_REQUEST
                )
        if request.user.is_authenticated and str(request.user.user_id) not in participant_ids:
            participant_ids.append(str(request.user.user_id))

        users = []
        for user_id in participant_ids:
            try:
                user = User.objects.get(user_id=user_id)
                users.append(user)
            except User.DoesNotExist:
                return Response({"detail": f"User with ID {user_id} not found."},
                                status=status.HTTP_400_BAD_REQUEST)

        # Create the conversation
        conversation = Conversation.objects.create()
        conversation.participants.set(users)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='send-message')
    def send_message(self, request, pk=None):
        """
        Custom action to send a message to an existing conversation.
        Requires 'message_body' in the request data.
        The sender is automatically set to the authenticated user.
        """
        conversation = get_object_or_404(Conversation, pk=pk)

        # Ensure the authenticated user is a participant in this conversation
        if not request.user.is_authenticated or request.user not in conversation.participants.all():
            return Response({"detail": "You do not have permission to send messages to this conversation."},
                            status=status.HTTP_403_FORBIDDEN)

        message_body = request.data.get('message_body')

        if not message_body:
            return Response({"detail": "Message body cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)

        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,  # Set the sender to the authenticated user
            message_body=message_body
        )
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed.
    Messages are typically created via the conversation's send_message action.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    # Only authenticated users can view messages.
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users can only see messages in conversations they are a part of.
        if self.request.user.is_authenticated:
            # Get conversations the user is a participant of
            user_conversations = self.request.user.conversations.all()
            # Filter messages to only those within those conversations
            return Message.objects.filter(conversation__in=user_conversations).order_by('sent_at')
        return Message.objects.none()

    def create(self, request, *args, **kwargs):
        # Disallow direct creation of messages from this endpoint.
        # Messages should be sent via the conversation's /send-message/ endpoint.
        return Response({"detail": "Messages should be sent via the conversation's /send-message/ endpoint."},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        # Allow only the sender to delete their own message.
        message = self.get_object()
        if request.user == message.sender:
            return super().destroy(request, *args, **kwargs)
        return Response({"detail": "You do not have permission to delete this message."},
                        status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        # Allow only the sender to update their own message.
        message = self.get_object()
        if request.user == message.sender:
            return super().update(request, *args, **kwargs)
        return Response({"detail": "You do not have permission to update this message."},
                        status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, *args, **kwargs):
        # Allow only the sender to partially update their own message.
        message = self.get_object()
        if request.user == message.sender:
            return super().partial_update(request, *args, **kwargs)
        return Response({"detail": "You do not have permission to update this message."},
                        status=status.HTTP_403_FORBIDDEN)
        


