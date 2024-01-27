from typing import TYPE_CHECKING
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

from core.models import BaseModel

# Create your models here.
if TYPE_CHECKING:
    from friends.models import FriendRequest, UserFriend


class User(BaseModel, AbstractUser):
    objects: UserManager["User"]

    sent_requests: models.Manager["FriendRequest"]
    received_requests: models.Manager["FriendRequest"]

    friends: models.Manager["UserFriend"]
    friends_of: models.Manager["UserFriend"]
