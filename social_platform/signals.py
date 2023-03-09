# inbuilt django signals
from django.core.signals import request_finished
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete

# custom signals
import django.dispatch
new_following = django.dispatch.Signal()

# decorator for receiving signals
from django.dispatch import receiver

# models
from .models import Post, Comment, Reaction, Activity, Following
from django.contrib.contenttypes.models import ContentType




# ----EXAMPLE----
# <sender> points to the model to listen to. None by default, meaning it listens to all.
@receiver(request_finished, sender=None, dispatch_uid='unique-string-to-protect-against-duplicate-signal')
def my_callback(sender, **kwargs):
    print(f'\n\n\nEXECUTED SIGNAL:  Request Finished!!!\n\n\n')


@receiver(new_following, sender=None, dispatch_uid='follow-uid')
@receiver(post_save, sender=Post, dispatch_uid='post-uid')
@receiver(post_save, sender=Comment, dispatch_uid='comment-uid')
@receiver(post_save, sender=Reaction, dispatch_uid='reaction-uid')
def activity_listener(sender, **kwargs):
    model_instance = kwargs.get('instance')
    newly_created = kwargs.get('created')

    model_name = type(model_instance).__name__
    content_type = ContentType.objects.get(model=model_name.lower())
    model_class = content_type.model_class()

    # only create an activity instance IF this activity is fresh (new post, 
    # new comment, new reaction, new following).
    if newly_created:
        # create activity for this reaction
        activity = Activity(
        content_type=content_type,
        object_id=model_instance.id,
        content_object=model_instance,
        )
        activity.save()

        # print(f'\n\n\nEXECUTED SIGNAL:  [{model_name}] activity created\n\n\n')



@receiver(post_delete, sender=Following, dispatch_uid='unfollow-uid')
@receiver(post_delete, sender=Post, dispatch_uid='post-delete-uid')
@receiver(post_delete, sender=Comment, dispatch_uid='comment-delete-uid')
@receiver(post_delete, sender=Reaction, dispatch_uid='unreact-uid')
def activity_destroy_listener(sender, **kwargs):
    model_instance = kwargs.get('instance')

    model_name = type(model_instance).__name__
    content_type = ContentType.objects.get(model=model_name.lower())
    model_class = content_type.model_class()

    # delete corresponding activity data linked to content
    Activity.objects.get(
        object_id=model_instance.id,
        content_type=content_type
    ).delete()    

    # print(f"[{model_name}] activity removed")
