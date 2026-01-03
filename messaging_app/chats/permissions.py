from rest_framework import permissions

class IsParticipant(permissions.BasePermission):
    """
    custom permission to allow only the participant of a chat to access it.
    """
    def has_object_permission(self, request, view, obj):
        # Assuming 'obj' is a Chat instance with a 'participants' ManyToMany field
        if hasattr(obj, 'participants'):
            return obj.sender == request.user
        
        if hasattr(obj, 'participants'):
            return obj.participants.filter(id=request.user.id).exists()
        
        return False
