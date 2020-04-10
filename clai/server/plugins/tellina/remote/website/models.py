from django.contrib import admin
from django.db import models
from django.utils import timezone

import datetime

class NL(models.Model):
    """
    Natural language command.
    """
    str = models.TextField(primary_key=True)

class Command(models.Model):
    """
    Command line.
    """
    str = models.TextField(primary_key=True)
    template = models.TextField(default='')
    language = models.TextField(default='bash')
    tags = models.ManyToManyField('Tag')

class CommandAdmin(admin.ModelAdmin):
    fields = ['str', 'language']
    list_display = ['get_str']

    def get_str(self, obj):
        return '\n'.join(obj.str)

class Tag(models.Model):
    """
    Tag.
    """
    str = models.TextField(primary_key=True)
    commands = models.ManyToManyField('Command')
    annotations = models.ManyToManyField('Annotation')

class URL(models.Model):
    """
    URL.

    :member str: url address.
    :member html_content: snapshot of the URL content at the time of annotation.
    :member commands: commands in the URL (automatically extracted)
    :member tags: tags of the URL (assigned based on user annotations)
    """
    str = models.TextField(primary_key=True)
    html_content = models.TextField(default='')
    commands = models.ManyToManyField('Command')
    tags = models.ManyToManyField('Tag')

class URLTag(models.Model):
    """
    Each record stores a (url, tag) pair.
    """
    url = models.ForeignKey(URL, on_delete=models.CASCADE)
    tag = models.TextField()

class User(models.Model):
    """
    Each record stores the information of a user.

    :member is_annotator: the annotator is responsible for collecting new data
        pairs
    :member is_judger: the judger is responsible for judging if a command pair
        is correct and add modifications and comments.
    """
    access_code = models.TextField(default='')
    ip_address = models.TextField(default='')
    first_name = models.TextField(default='anonymous')
    last_name = models.TextField(default='anonymous')
    organization = models.TextField(default='--')
    city = models.TextField(default='--')
    region = models.TextField(default='--')
    country = models.TextField(default='--')
    is_annotator = models.BooleanField(default=False)
    is_judger = models.BooleanField(default=False)
    time_logged = models.FloatField(null=True, blank=True)

class UserAdmin(admin.ModelAdmin):
    fields = ['first_name', 'last_name', 'is_annotator', 'is_judger']
    list_display = ['get_full_name']

    def get_full_name(self, obj):
        return '\n'.join(obj.first_name + obj.last_name)


class Annotation(models.Model):
    """
    Each record is a natural language <-> code translation annotated by a
    programmer.
    """
    url = models.ForeignKey(URL, on_delete=models.CASCADE)
    nl = models.ForeignKey(NL, on_delete=models.CASCADE)
    cmd = models.ForeignKey(Command, on_delete=models.CASCADE)
    annotator = models.ForeignKey(User, on_delete=models.CASCADE)
    submission_time = models.DateTimeField(default=timezone.now)


class AnnotationProgress(models.Model):
    """
    Each record stores a user's annotation progress on a particular URL.
    """
    url = models.ForeignKey(URL, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, null=True, on_delete=models.CASCADE)
    annotator = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.TextField()


class Comment(models.Model):
    """
    Each record is a commend submitted by a user (either an annotator or a
    judger) to an annotation.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.ForeignKey('self', null=True, on_delete=models.CASCADE)
    str = models.TextField()
    submission_time = models.DateTimeField(default=timezone.now)


class AnnotationUpdate(models.Model):
    """
    Each record is an update of an annotation submitted by a judger.
    """
    annotation = models.ForeignKey(Annotation, on_delete=models.CASCADE)
    judger = models.ForeignKey(User, on_delete=models.CASCADE)
    update_str = models.TextField()
    update_type = models.TextField(default='nl')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    submission_time = models.DateTimeField(default=timezone.now)
    status = models.TextField(default='open')


class Notification(models.Model):
    """
    Each record is a certain type of message issued from one annotator to
    another.
    """
    sender = models.ForeignKey(User, related_name='notification_sender',
                               on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='notification_receiver',
                                 on_delete=models.CASCADE)
    type = models.TextField(default='comment')
    annotation_update = models.ForeignKey('AnnotationUpdate', null=True,
                                          on_delete=models.CASCADE)
    comment = models.ForeignKey('Comment', null=True, on_delete=models.CASCADE)
    url = models.ForeignKey('URL', on_delete=models.CASCADE)
    creation_time = models.DateTimeField(default=timezone.now)
    status = models.TextField(default='issued')


class Translation(models.Model):
    """
    Each record is a natural language -> code translation generated by the
    learning module in the backend.

    :member request: the natural language request issued by the user
    :member pred_cmd: the predicted command generated by the learning module
    :member score: the translation score of the predicted command
    :member num_upvotes: number of upvotes this translation has received
    :member num_downvotes: number of downvotes this translation has received
    :member num_stars: number of stars this translation has received
    """
    nl = models.ForeignKey(NL, on_delete=models.CASCADE)
    pred_cmd = models.ForeignKey(Command, on_delete=models.CASCADE)
    score = models.FloatField()
    num_upvotes = models.PositiveIntegerField(default=0)
    num_downvotes = models.PositiveIntegerField(default=0)
    num_stars = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "{}\n{}".format(self.request, self.pred_cmd)

    def inc_num_upvotes(self):
        self.num_upvotes += 1

    def dec_num_upvotes(self):
        self.num_upvotes -= 1

    def inc_num_downvotes(self):
        self.num_downvotes += 1

    def dec_num_downvotes(self):
        self.num_downvotes -= 1

    def inc_num_stars(self):
        self.num_stars += 1

    def dec_num_stars(self):
        self.num_stars -= 1

    @property
    def num_votes(self):
        return self.num_upvotes - self.num_downvotes


class NLRequest(models.Model):
    """
    Each record stores the IP address associated with a natural language
    request.
    :member request: a natural language request
    :member user: the user who submitted the request
    :member submission_time: the time when the request is submitted
    """
    nl = models.ForeignKey(NL, on_delete=models.CASCADE)
    submission_time = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)


class Vote(models.Model):
    """
    Each record stores the voting actions to a translation results issued by a
    specific IP address.
    """
    translation = models.ForeignKey(Translation, on_delete=models.CASCADE)
    ip_address = models.TextField(default='')
    upvoted = models.BooleanField(default=False)
    downvoted = models.BooleanField(default=False)
    starred = models.BooleanField(default=False)
    # user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
