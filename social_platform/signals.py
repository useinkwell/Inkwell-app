# inbuilt django signals
from django.core.signals import request_finished
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete

# custom signals
import django.dispatch
new_following = django.dispatch.Signal()

# decorator for receiving signals
from django.dispatch import receiver

# models
from .models import Post, Comment, Reaction, Activity
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
    print(kwargs)

    model_name = type(model_instance).__name__
    content_type = ContentType.objects.get(model=model_name.lower())
    model_class = content_type.model_class()

    # only create an activity instance IF this activity is fresh content
    # (new post, new comment, new reaction). Exception would be made for new
    # follower activity, since no new model instance is created by it
    if newly_created:
        # create activity for this reaction
        activity = Activity(
        content_type=content_type,
        object_id=model_instance.id,
        content_object=model_instance,
        )
        activity.save()

        print(f'\n\n\nEXECUTED SIGNAL:  {model_name} Event Occured\n\n\n')
