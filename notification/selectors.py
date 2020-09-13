from .models import Notification


def get_user_notifications(user):
    notifications = Notification.objects.filter(user=user, status="Unread")
    return notifications


def get_notification(notification_id):
    notification = Notification.objects.get(pk=notification_id)
    return notification


def get_all_notifications(user):
    return user.notification_set.all()


def read_all_notifications(user):
    notifications = get_all_notifications(user)
    notifications.filter(user=user).update(status="Read")
    return notifications


def get_recent_notification(user):
    notifications = get_all_notifications(user)
    if notifications:
        return notifications.order_by('-id')
    else:
        return []


