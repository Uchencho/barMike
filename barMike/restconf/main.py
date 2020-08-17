import datetime
from datetime import timedelta

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'accounts.api.utils.custom_exception_handler',

    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'rest_framework.authentication.SessionAuthentication',
        'accounts.api.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
        # 'accounts.api.permissions.IsTokenValid',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.SearchFilter',
        # 'rest_framework.filters.OrderingFilter',
    ],
    'SEARCH_PARAM':'search',
    # 'ORDERING_PARAM':'ordering',
}