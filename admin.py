from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from .models import Profile, ProfileOrganization, InviteCampaign, InviteBatch
from .models import InviteBatchRecipient, ProfileMember, ProfileSubCommunity


from .models import ContentTopic, ContentTopicFollow, ContentItem, ContentItemTopic, ContentItemParticipation
from .models import ContentItemHash, ContentFollow, ContentItemEmbed, ContentItemComment


admin.site.register(Profile)
admin.site.register(ProfileOrganization)
admin.site.register(InviteCampaign)
admin.site.register(InviteBatch)

admin.site.register(InviteBatchRecipient)
admin.site.register(ProfileMember)
admin.site.register(ProfileSubCommunity)


admin.site.register(ContentTopic)
admin.site.register(ContentTopicFollow)
admin.site.register(ContentItem)
admin.site.register(ContentItemTopic)
admin.site.register(ContentItemParticipation)
admin.site.register(ContentItemHash)
admin.site.register(ContentFollow)
admin.site.register(ContentItemEmbed)
admin.site.register(ContentItemComment)

