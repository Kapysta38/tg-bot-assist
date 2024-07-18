from ..api import APIClient


def get_reg_func(obj):
    """
    Функция для получения списка всех методов начинающихся на `reg_`
    :param obj: Класс
    :return:
    """
    result = []
    method_list = [method for method in dir(obj) if method.startswith('reg_')]
    for method in method_list:
        result.append(getattr(obj, method))
    return result


async def get_users_in_chat_role(client: APIClient):
    # Получаем все роли с именем "chat"
    roles = await client.get_filter_roles(role_name="chat")
    chat_role_ids = [role['role_id'] for role in roles]

    tg_ids = []
    # Проходим по каждой роли "chat" и ищем пользователей с этой ролью
    for role_id in chat_role_ids:
        user_roles = await client.get_filter_user_roles(role_id=role_id)
        user_ids = [user_role['user_id'] for user_role in user_roles]

        # Получаем пользователей и их tg_id
        for user_id in user_ids:
            user = await client.get_user(user_id=user_id)
            tg_ids.append(user['tg_id'])

    return tg_ids
