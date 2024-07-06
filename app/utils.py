from datetime import datetime, timedelta
from django.db.models import Sum, Q
from django.conf import settings
from .models import Box


def get_average_area():
    total_area = Box.objects.aggregate(Sum('area'))['area__sum'] or 0
    count = Box.objects.count() or 1
    return total_area / count


def get_user_average_volume(user):
    total_volume = Box.objects.filter(creator=user).aggregate(
        Sum('volume'))['volume__sum'] or 0
    count = Box.objects.filter(creator=user).count() or 1
    return total_volume / count


def get_total_boxes_in_last_week():
    one_week_ago = datetime.now() - timedelta(days=7)
    return Box.objects.filter(created_at__gte=one_week_ago).count()


def get_user_total_boxes_in_last_week(user):
    one_week_ago = datetime.now() - timedelta(days=7)
    return Box.objects.filter(creator=user, created_at__gte=one_week_ago).count()


def check_constraints(user):
    if get_average_area() > settings.A1:
        return False, 'Average area of all boxes exceeds the limit.'
    if get_user_average_volume(user) > settings.V1:
        return False, 'Average volume of boxes added by you exceeds the limit.'
    if get_total_boxes_in_last_week() > settings.L1:
        return False, 'Total boxes added in the last week exceeds the limit.'
    if get_user_total_boxes_in_last_week(user) > settings.L2:
        return False, 'Total boxes added by you in the last week exceeds the limit.'
    return True, ''


def apply_filters(Boxes, request, isCreatedByUser=False):
    filter = {}
    # Length
    length_more_than = request.query_params.get('length_more_than', None)
    length_less_than = request.query_params.get('length_less_than', None)

    if length_more_than:
        filter['length__gt'] = length_more_than
    if length_less_than:
        filter['length__lt'] = length_less_than

    # Breadth
    breadth_more_than = request.query_params.get('breadth_more_than', None)
    breadth_less_than = request.query_params.get('breadth_less_than', None)

    if breadth_more_than:
        filter['breadth__gt'] = breadth_more_than
    if breadth_less_than:
        filter['breadth__lt'] = breadth_less_than

    # Height
    height_more_than = request.query_params.get('height_more_than', None)
    height_less_than = request.query_params.get('height_less_than', None)

    if height_more_than:
        filter['height__gt'] = height_more_than
    if height_less_than:
        filter['height__lt'] = height_less_than

    # Area
    area_more_than = request.query_params.get('area_more_than', None)
    area_less_than = request.query_params.get('area_less_than', None)

    if area_more_than:
        filter['area__gt'] = area_more_than
    if area_less_than:
        filter['area__lt'] = area_less_than

    # Volume
    volume_more_than = request.query_params.get('volume_more_than', None)
    volume_less_than = request.query_params.get('volume_less_than', None)

    if volume_more_than:
        filter['volume__gt'] = volume_more_than
    if volume_less_than:
        filter['volume__lt'] = volume_less_than

    if not isCreatedByUser:
        # user
        username = request.query_params.get('username', None)
        if username:
            filter['creator__username'] = username

        # date
        created_after = request.query_params.get('created_after', None)
        created_before = request.query_params.get('created_before', None)

        if created_after:
            filter['created_at__gt'] = created_after
        if created_before:
            filter['created_at__lt'] = created_before

    if filter:
        q_object = Q(**filter)
        Boxes = Boxes.filter(q_object)

    return Boxes
