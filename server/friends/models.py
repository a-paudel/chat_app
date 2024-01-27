from django.db import models
from django.core.exceptions import ValidationError
from core.models import BaseModel
from users.models import User


# Create your models here.
class FriendRequest(BaseModel):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_friend_requests")
    sender_id: int
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_friend_requests")
    receiver_id: int

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["sender", "receiver"], name="friend_request_unique"),
            models.CheckConstraint(check=~models.Q(sender=models.F("receiver")), name="friend_request_not_self"),
        ]

    def clean(self) -> None:
        # check if receiver has already sent a friend request to sender
        is_reverse_request_exists = FriendRequest.objects.filter(sender=self.receiver, receiver=self.sender).exists()
        if is_reverse_request_exists:
            raise ValidationError({"receiver_id": "Friend request already exists"})
        return super().clean()


class UserFriend(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friends")
    user_id: int
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friends_of")
    friend_id: int

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "friend"], name="user_friend_unique"),
            models.CheckConstraint(check=~models.Q(user=models.F("friend")), name="user_friend_not_self"),
        ]

    def clean(self) -> None:
        # check if already friends
        is_already_friends = UserFriend.objects.filter(
            (models.Q(user=self.user) & models.Q(friend=self.friend))
            | (models.Q(user=self.friend) & models.Q(friend=self.user))
        ).exists()

        if is_already_friends:
            raise ValidationError({"friend_id": "Already friends"})
        return super().clean()
