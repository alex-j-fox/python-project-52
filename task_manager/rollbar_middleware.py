from rollbar.contrib.django.middleware import RollbarNotifierMiddleware


class CustomRollbarNotifierMiddleware(RollbarNotifierMiddleware):
    # def get_extra_data(self, request, exc):
    #     """
    #     Возвращает дополнительные данные для отчетов Rollbar.

    #     :param request: Текущий запрос.
    #     :type request: HttpRequest
    #     :param exc: Исключение, вызвавшее отчет.
    #     :type exc: Exception
    #     :return: Дополнительные данные для отчета.
    #     :rtype: dict
    #     """
    #     extra_data = dict()

    #     # Добавьте дополнительные данные в отчет
    #     extra_data['trace_id'] = 'aabbccddeeff'
    #     # Add a list of feature flags
    #     extra_data['feature_flags'] = [
    #         'feature_1',
    #         'feature_2',
    #     ]

    #     return extra_data

    def get_payload_data(self, request, exc):
        """
        Возвращает данные о пользователе, инициировавшем отчет.

        :param request: Текущий запрос.
        :type request: HttpRequest
        :param exc: Исключение, вызвавшее отчет.
        :type exc: Exception
        :return: Данные о пользователе.
        :rtype: dict
        """
        payload_data = dict()

        if not request.user.is_anonymous:
            payload_data = {
                'person': {
                    'id': request.user.id,
                    'username': request.user.username,
                    'email': request.user.email,
                    'full_name': request.user.get_full_name(),
                },
            }

        return payload_data
