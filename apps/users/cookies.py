from django.conf import settings


ACCESS = "unilink_access"
REFRESH = "unilink_refresh"


def set_auth_cookies(response, access, refresh=None):
    """Функция для установки куки аутентицикации"""
    opts = {
        "httponly": True,
        "samesite": "Lax",
        "secure": settings.COOKIE_SECURE,
    } # Параметры безопастности

    response.set_cookie(
        ACCESS, access,
        max_age=int(settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()),
        **opts
    )

    if refresh:
        response.set_cookie(
                REFRESH, refresh,
                max_age=int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds()),
                **opts
            )


def clear_auth_cookies(response):
    """Функция для удаления куки"""
    for name in (ACCESS, REFRESH):
        response.delete_cookie(name, samesite="Lax")
