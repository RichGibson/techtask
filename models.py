import sys
from datetime import datetime

from django.db import models
from djorm_pgarray.fields import ArrayField
from djorm_expressions.models import ExpressionManager

from datetime import datetime, timedelta



import operator
from numpy import mean, median,  std, array

def sort_by_posts(d):
    """ task2.2 Write a function that returns a list of objects with the following structure:
        first_name, last_name, posts, ordered by number of posts, removing any users that have not made any posts.
    """
    rslt = [ {'first_name':u['name'].split()[0], 'last_name':u['name'].split()[-1], 'posts':u['posts']} for u in d if u['posts'] > 0 ]
    rslt.sort(key=operator.itemgetter('posts'))
    rslt.reverse()
    return rslt

def stats(d):
    """ task2.3 write a function to generate the average, median, max, min, and standard deviation of number 
        of posts
    """
    lst  = array([u['posts'] for u in d] )
    rslt = {'average':mean(lst),'median':median(lst), 'max': max(lst), 'min':min(lst), 'std':std(lst)}
    return rslt

def readable_date(dt):
    """ The database interface we use within our python layer (psycopg2)
        returns objects of type datetime.datetime (http://docs.python.org/2/library/ datetime.html) 
        for any fields that are timestamps. Write a function that takes in a datetime.datetime and 
        returns one of the following values:
         Just now
         [x] minute(s) ago
         [y] hour(s) ago
         [z] day(s) ago
         [a] week(s) ago
         [b] month(s) ago
         [c] months(s) ago
    """

    delta = datetime.now() - dt

    # This should possibly consider leap years. 
    if (delta.days//365 >0):
        return "[%i] year(s) ago" % (delta.days//365)

    # I know enough to know this is wrong, but it is more or less correct on average 
    # An average month is 30.4 days. 
    if (delta.days//30 >0):
        return "[%i] month(s) ago" % (delta.days//30)

    if (delta.days//7 >0):
        return "[%i] week(s) ago" % (delta.days//7)

    if (delta.days//1 >0):
        return "[%i] day(s) ago" % (delta.days//1)

    if (delta.seconds//3600 >0):
        return "[%i] hour(s) ago" % (delta.seconds//3600)

    if (delta.seconds//60 >0):
        return "[%i] minute(s) ago" % (delta.seconds//60)

    return "Just now"



class Profile(models.Model):
    type = ArrayField(dbtype="varchar(31)")
    follower_count = models.IntegerField()
    groups = models.IntegerField()
    created  = models.DateTimeField() # should not have time zone
    last_active  = models.DateTimeField() # should not have time zone

    class Meta:
        db_table="profile"

    def save(self, *args, **kwargs):
        """update timestamps, using auto_now_add and auto_now may make the table not 
           appear in the admin, so just avoid that drama"""
        if not self.id:
            self.created=datetime.now()
        last_active = datetime.now()
        return super(Profile, self).save(*args, **kwargs)

class ProfileOrganization(models.Model):
    profile = models.ForeignKey(Profile)
    name = models.CharField(max_length=255)
    url_name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.CharField(max_length=255)
    active = models.BooleanField()
    created  = models.DateTimeField() # should not have time zone
    updated  = models.DateTimeField() # should not have time zone
    website = models.CharField(max_length=255)
    size = models.CharField(max_length=63)
    alt_names = ArrayField(dbtype="varchar(255)")
    email_domains = ArrayField(dbtype="varchar(255)")

    class Meta:
        db_table="profile_organization"

    def save(self, *args, **kwargs):
        """update timestamps, using auto_now_add and auto_now may make the table not 
           appear in the admin, so just avoid that drama"""
        if not self.id:
            self.created=datetime.now()
        self.updated = datetime.now()
        return super(ProfileOrganization, self).save(*args, **kwargs)

    
class InviteCampaign(models.Model):
    owner = models.ForeignKey(ProfileOrganization, blank=True)
    name     = models.CharField(max_length=255)
    follows  = ArrayField(dbtype="integer")
    alt_names = ArrayField(dbtype="varchar(255)")
    segments = ArrayField(dbtype="integer")
    memberships = ArrayField(dbtype="integer")
    roles    = ArrayField(dbtype="varchar[255]")
    created  = models.DateTimeField() # should not have time zone
    updated  = models.DateTimeField() # should not have time zone
    type     = models.CharField(max_length=60)
    active   = models.BooleanField()
    linkable = models.BooleanField()

    class Meta:
        db_table="invite_campaign"

    def save(self, *args, **kwargs):
        """update timestamps, using auto_now_add and auto_now may make the table not 
           appear in the admin, so just avoid that drama"""
        if not self.id:
            self.created=datetime.now()
        self.updated = datetime.now()
        return super(InviteCampaign, self).save(*args, **kwargs)

class InviteBatch(models.Model):
    campaign = models.ForeignKey(InviteCampaign)
    groups = ArrayField(dbtype="integer")
    created  = models.DateTimeField() # should not have time zone
    updated  = models.DateTimeField() # should not have time zone

    class Meta:
        db_table="invite_batch"

    def save(self, *args, **kwargs):
        """update timestamps, using auto_now_add and auto_now may make the table not 
           appear in the admin, so just avoid that drama"""
        if not self.id:
            self.created=datetime.now()
        self.updated = datetime.now()
        return super(InviteBatch, self).save(*args, **kwargs)


class InviteBatchRecipient(models.Model):
    member = models.ForeignKey(Profile,blank=True, null=True)
    batch  = models.ForeignKey(InviteBatch)
    email = models.CharField(max_length=255)
    key = models.CharField(max_length=1024)
    expired = models.BooleanField(default=False)
    name = models.CharField(max_length=127)
    used = models.BooleanField(default=False)
    created  = models.DateTimeField() # should not have time zone
    updated  = models.DateTimeField() # should not have time zone

    class Meta:
        db_table="invite_batch_recipient"

    def save(self, *args, **kwargs):
        """update timestamps, using auto_now_add and auto_now may make the table not 
           appear in the admin, so just avoid that drama"""
        if not self.id:
            self.created=datetime.now()
        self.updated = datetime.now()
        return super(InviteBatchRecipient, self).save(*args, **kwargs)

class ProfileMember(models.Model):
    profile = models.ForeignKey(Profile)
    identity = models.IntegerField() # this seems like a key to something?
    first_name = models.CharField(max_length=127)
    last_name = models.CharField(max_length=127)
    summary = models.CharField(max_length=255)
    biography = models.TextField()
    image = models.CharField(max_length=255)
    active = models.BooleanField()
    security_clearance = models.CharField(max_length=512)
    digest_subscribe = models.BooleanField()
    created  = models.DateTimeField() # should not have time zone
    updated  = models.DateTimeField() # should not have time zone
    digest_sent  = models.DateTimeField() # should not have time zone

    class Meta:
        db_table="profile_member"

    def save(self, *args, **kwargs):
        """update timestamps, using auto_now_add and auto_now may make the table not 
           appear in the admin, so just avoid that drama"""
        if not self.id:
            self.created=datetime.now()
        self.updated = datetime.now()
        return super(ProfileMember, self).save(*args, **kwargs)

class ProfileSubCommunity(models.Model):
    profile = models.ForeignKey(Profile)
    name = models.CharField(max_length=50)
    parent_name = models.CharField(max_length=127)
    parent_id = models.ForeignKey(Profile,related_name="profile_sub_community_parent")
    description = models.TextField() 
    image = models.CharField(max_length=255)
    active = models.BooleanField()
    private = models.BooleanField()
    email_domains = ArrayField(dbtype="varchar(64)")
    website = models.CharField(max_length=255)
    created  = models.DateTimeField() # should not have time zone
    updated  = models.DateTimeField() # should not have time zone

    class Meta:
        db_table="profile_sub_community"

    def save(self, *args, **kwargs):
        """update timestamps, using auto_now_add and auto_now may make the table not 
           appear in the admin, so just avoid that drama"""
        if not self.id:
            self.created=datetime.now()
        self.updated = datetime.now()
        return super(ProfileSubCommunity, self).save(*args, **kwargs)



class ContentTopic(models.Model):
    name = models.CharField(max_length=510)
    follower_count = models.IntegerField()
    created  = models.DateTimeField() # should not have time zone
    updated  = models.DateTimeField() # should not have time zone

    class Meta:
        db_table="content_topic"

    def save(self, *args, **kwargs):
        """update timestamps, using auto_now_add and auto_now may make the table not 
           appear in the admin, so just avoid that drama"""
        if not self.id:
            self.created=datetime.now()
        self.updated = datetime.now()
        return super(ContentTopic, self).save(*args, **kwargs)

class ContentTopicFollow (models.Model):
    topic = models.ForeignKey(ContentTopic)
    profile = models.ForeignKey(Profile)
    profile_type = models.CharField(max_length=62)
    created  = models.DateTimeField() # should not have time zone

    class Meta:
        db_table="content_topic_follow"

    def save(self, *args, **kwargs):
        """update timestamps, using auto_now_add and auto_now may make the table not 
           appear in the admin, so just avoid that drama"""
        if not self.id:
            self.created=datetime.now()
        return super(ContentTopicFollow, self).save(*args, **kwargs)



class ContentItem(models.Model):
    type = models.CharField(max_length=63)
    pending = models.BooleanField()
    source = models.CharField(max_length=63)
    author = models.IntegerField()
    author_type = models.CharField(max_length=63)
    message = models.TextField()
    slug = models.CharField(max_length=200)
    recipient = models.IntegerField()
    recipient_type = models.CharField(max_length="63")
    like_count = models.IntegerField()
    comment_count = models.IntegerField()
    learn_count = models.IntegerField()
    private = models.BooleanField()
    title = models.TextField()
    segments  = ArrayField(dbtype="integer")
    created  = models.DateTimeField() # should not have time zone
    updated  = models.DateTimeField() # should not have time zone

    class Meta:
        db_table="content_type"

    def save(self, *args, **kwargs):
        """update timestamps, using auto_now_add and auto_now may make the table not 
           appear in the admin, so just avoid that drama"""
        if not self.id:
            self.created=datetime.now()
        self.updated = datetime.now()
        return super(ContentItem, self).save(*args, **kwargs)

class ContentItemTopic(models.Model):
    topic = models.ForeignKey(ContentTopic)
    item = models.ForeignKey(ContentItem)

    class Meta:
        db_table="content_item_topic"

class ContentItemParticipation(models.Model):
    item = models.ForeignKey(ContentItem)
    profile  = models.ForeignKey(Profile)
    profile_type = models.CharField(max_length=62)
    comment_id = models.IntegerField()
    
    liked  = models.DateTimeField() # should not have time zone
    learned  = models.DateTimeField(blank=True, null=True) # should not have time zone
    hidden  = models.DateTimeField(blank=True, null=True) # should not have time zone
    flagged  = models.DateTimeField(blank=True, null=True) # should not have time zone
    posted  = models.DateTimeField(blank=True, null=True) # should not have time zone
    updated  = models.DateTimeField(blank=True, null=True) # should not have time zone

    class Meta:
        db_table="content_item_participation"

    def save(self, *args, **kwargs):
        """update timestamps, using auto_now_add and auto_now may make the table not 
           appear in the admin, so just avoid that drama.
            Not sure how to handle the liked/learned/hidden/flagged stamps"""
        if not self.id:
            self.posted=datetime.now()
        self.updated = datetime.now()
        return super(ContentItemParticipation, self).save(*args, **kwargs)

class ContentItemHash(models.Model):
    item = models.ForeignKey(ContentItem)
    hash = models.CharField(max_length=64)

    class Meta:
        db_table="content_item_hash"

class ContentFollow(models.Model):
    """ not sure why I need this """
    follower_id = models.IntegerField()
    target_id  = models.IntegerField()
    follower_type = models.CharField(max_length=62)
    created  = models.DateTimeField() # should not have time zone
    updated  = models.DateTimeField() # should not have time zone

    class Meta:
        db_table="content_follow"

    def save(self, *args, **kwargs):
        """update timestamps, using auto_now_add and auto_now may make the table not 
           appear in the admin, so just avoid that drama"""
        if not self.id:
            self.created=datetime.now()
        self.updated = datetime.now()
        return super(ContentFollow, self).save(*args, **kwargs)

class ContentItemEmbed(models.Model):
    item = models.ForeignKey(ContentItem)
    type = models.CharField(max_length=62)
    title = models.CharField(max_length=510)
    description = models.TextField()
    source_url = models.CharField(max_length=2046)
    url = models.CharField(max_length=2046)
    thumbnail_url = models.CharField(max_length=2046)
    thumbnail_height = models.IntegerField()
    thumbnail_width = models.IntegerField()
    html  = models.TextField()
    height = models.IntegerField()
    width = models.IntegerField()

    class Meta:
        db_table="content_item_embed"

class ContentItemComment(models.Model):
    itemd = models.ForeignKey(ContentItem)
    author_id = models.IntegerField() # does author_id points at profile?
    author_type = models.CharField(max_length=62) 
    message = models.TextField()
    like_count = models.IntegerField()
    created  = models.DateTimeField() # should not have time zone
    updated  = models.DateTimeField() # should not have time zone

    class Meta:
        db_table="content_item_comment"

    def save(self, *args, **kwargs):
        """update timestamps, using auto_now_add and auto_now may make the table not 
           appear in the admin, so just avoid that drama"""
        if not self.id:
            self.created=datetime.now()
        self.updated = datetime.now()
        return super(content_item_comment, self).save(*args, **kwargs)
