from operator import attrgetter


def checksecurity(pg_type, user_info):
    ext = False
    user_type, value_status = attrgetter('user_type', 'status')(user_info)
    if value_status == 0:
        ext = True
    if pg_type == 1:
        if user_type == 0:
            ext = True

    return ext
