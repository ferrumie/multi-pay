from rest_framework import permissions
from django.core.cache import cache


class IsOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners to have access to the requests
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsIdempotent(permissions.BasePermission):
    message = 'Duplicate request detected.'

    def has_permission(self, request, view):
        if request.method != 'POST':
            return True
        ival = request.META.get('HTTP_X_IDEMPOTENCY_KEY')
        if ival is None:
            return True
        ival = ival[:128]
        key = 'idemp-{}-{}'.format(request.user.pk, ival)
        is_idempotent = bool(cache.add(key, 'yes',
                                       1000))
        # if not is_idempotent:
        #     logger.info(u'Duplicate request (non-idempotent): %s', key)
        return is_idempotent
