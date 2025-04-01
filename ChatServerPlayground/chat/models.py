from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your   models here.


#  model for user relation
class UserRelation(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,
                             related_name='user_relations')
    friend = models.ForeignKey(User,on_delete=models.CASCADE,
                               default=None,related_name='friend_relations')
    accepted = models.BooleanField(default=False)
    relation_key = models.CharField(max_length=255,blank=True,null=True)
    
    # str method
    def __str__(self):
        return f'{self.user.username}-{self.friend}'
    
    
# model for the message
class Message(models.Model):
    description = models.TextField()
    sender_name = models.ForeignKey(User,on_delete=models.CASCADE,
                                    related_name='sender')
    receiver_name = models.ForeignKey(User,on_delete=models.CASCADE,
                                      related_name='receiver')
    time = models.TimeField(auto_now_add=True)
    seen = models.BooleanField(default=True)
    timestamp = models.DateTimeField(default=timezone.now,blank=True)
    
    class Meta:
        ordering = ('timestamp',)

