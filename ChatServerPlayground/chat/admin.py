from django.contrib import admin
from .models import Message, UserRelation
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Register your models here.

# Message Admin
class MessageAdmin(admin.ModelAdmin):
    list_display = ["sender_name","receiver_name","seen","time"]
    list_filter = ["sender_name","receiver_name","seen"]
    search_fields = ["sender_name__username","receiver_name__username","description"]
    
# registering the Message and MessageAdmin
admin.site.register(Message,MessageAdmin)



# building the custom user model for display
class CustomUserAdmin(UserAdmin):
    list_display = ["id","username","email","first_name","last_name","is_staff","date_joined"]


# unregister the default user
admin.site.unregister(User)


# Register the user, custom user model
admin.site.register(User,CustomUserAdmin)


# Creating the user relation model
class UserRelationAdmin(admin.ModelAdmin):
    list_display = ["id","user","friend","accepted"]
    list_filter = ["user","accepted"]
    search_fields = ["user__username","friend"]
    
# registering the admin
admin.site.register(UserRelation,UserRelationAdmin)
