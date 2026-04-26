from .models import Channel, Subscription

def user_channel(request):
    channel = None
    subscribers_count = 0
    subscriptions = []
    user_id = request.session.get('user_id')
    if user_id:
        channel = Channel.objects.filter(owner_id=user_id).first()
        if channel:
            subscribers_count = Subscription.objects.filter(channel=channel).count()
        subscriptions = list(
            Subscription.objects.filter(subscriber_id=user_id)
            .select_related('channel')
            .order_by('-created_at')
        )
    return {
        'user_channel': channel,
        'user_channel_subscribers': subscribers_count,
        'user_subscriptions': subscriptions,
    }