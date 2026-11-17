from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed, TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from . import cookies


class JWTCookieMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        Перехватывает входящий HTTP-запрос
        для реализации JWT-аутентификации
        """
        auth = JWTAuthentication() # класс для валидации токенов
        access = request.COOKIES.get(cookies.ACCESS)
        refresh = request.COOKIES.get(cookies.REFRESH)

        renewed = None
        user = self._user(auth, access)

        # Если нет a-token или он недействителен, но есть r-token
        if user is None and refresh:
            try:
                renewed = str(RefreshToken(refresh).access_token)
            except TokenError:
                renewed = None

            if renewed:
                user = self._user(auth, renewed)
                request.COOKIES[cookies.ACCESS] = renewed

        if user is not None:
            request.user = user

        response = self.get_response(request)

        if cookies.ACCESS not in response.cookies:
            # Если токен был обновлён в `renewed`
            if renewed and user is not None:
                # Обновляе куки браузера
                cookies.set_auth_cookies(response, renewed)
            # Если с токенами что-то не так
            elif user is None and (access or refresh):
                # Очищаем куки браузера
                cookies.clear_auth_cookies(response)
        return response

    @staticmethod
    def _user(auth: JWTAuthentication, raw: str | None) -> User | None:
        """Преобразование сырой строки токена в объект пользователя"""
        if not raw:
            return None

        try:
            return auth.get_user(auth.get_validated_token(raw))
        except AuthenticationFailed:
            return None
