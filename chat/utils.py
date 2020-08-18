from channels.db import database_sync_to_async
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers.python import Serializer
from django.utils.encoding import smart_text 
from django.conf import settings

from .exceptions import ClientError
from .models import Room, RoomChatMessage


# This decorator turns this function from a synchronous function into an async one
# we can call from our async consumers, that handles Django DBs correctly.
# For more, see http://channels.readthedocs.io/en/latest/topics/databases.html
@database_sync_to_async
def get_room_or_error(room_id, user):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    # Check if the user is logged in
    # if not user.is_authenticated:
    #     raise ClientError("USER_HAS_TO_LOGIN", "You must login.")
    # Find the room they requested (by ID)
    try:
        room = Room.objects.get(pk=room_id)
    except Room.DoesNotExist:
        raise ClientError("ROOM_INVALID", "Invalid room.")
    # Check permissions
    if room.staff_only and not user.is_staff:
        raise ClientError("ROOM_ACCESS_DENIED", "You do not have permission to join this room.")
    return room



class LazyRoomChatMessageEncoder(Serializer):
    def get_dump_object(self, obj):
        dump_object = {}
        dump_object.update({'username': smart_text(obj.user.username, strings_only=True)})
        dump_object.update({'message': smart_text(obj.content, strings_only=True)})
        dump_object.update({'profile_image': smart_text(obj.user.profile_image.url, strings_only=True)})
        return dump_object









