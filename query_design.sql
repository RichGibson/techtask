select * from profile_member, profile, invite_batch_recipient, invite_batch, invite_campaign
where invite_campaign.owner_id = 500
    and invite_campaign.id = invite_batch.campaign_id
    and invite_batch.id = invite_batch_recipient.batch_id
    and invite_batch_recipient.member_id = profile.id
    and profile_member.profile_id=profile.id
    and profile_member.active = True;




select profile.id,
    sum(CASE when content_item_participation.posted > now() - interval '1 week' THEN 1 ELSE 0 END) as posts,
    sum(CASE when content_item_participation.liked > now() - interval '1 week' THEN 1 ELSE 0 END) as liked
    from profile, content_item_participation
    where content_item_participation.profile_id = profile.id
    and profile.id in
        (select profile.id from profile_member, profile, invite_batch_recipient, invite_batch, invite_campaign
        where invite_campaign.owner_id = 500
            and invite_campaign.id = invite_batch.campaign_id
            and invite_batch.id = invite_batch_recipient.batch_id
            and invite_batch_recipient.member_id = profile.id
            and profile_member.profile_id=profile.id
            and profile_member.active = True)
    group by profile.id
    order by profile.id


select count(*)
    from content_topic_follow
    where profile_id in
        (select profile.id from profile_member, profile, invite_batch_recipient, invite_batch, invite_campaign
            where invite_campaign.owner_id = 500
                and invite_campaign.id = invite_batch.campaign_id
                and invite_batch.id = invite_batch_recipient.batch_id
                and invite_batch_recipient.member_id = profile.id
                and profile_member.profile_id=profile.id
                and profile_member.active = True)

