from django import template
from juntagrico_polling.dao.pollingdao import PollingDao
from juntagrico.dao.memberdao import MemberDao

register = template.Library()

@register.simple_tag(takes_context=True)
def show_quick_vote(context):
    current_user = context['request'].user
    allowed_to_vote = PollingDao.is_member_with_shares(current_user) and not PollingDao.votes_from_user(current_user) and len(PollingDao.active_polls_ordered()) == 1
    return allowed_to_vote

@register.simple_tag()
def current_vote_id():
    return PollingDao.active_polls_ordered()[0].id