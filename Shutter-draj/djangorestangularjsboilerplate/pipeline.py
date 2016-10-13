def user_password(strategy, user, is_new=False, *args, **kwargs):
    if strategy.backend.name != 'email':
        return

    password = strategy.request_data()['password']
    if is_new:
        user.set_password(password)
        user.save()
    elif not user.validate_password(password):
        # return {'user': None, 'social': None}
        raise AuthException(strategy.backend)