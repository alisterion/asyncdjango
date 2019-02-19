from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, \
    HASH_SESSION_KEY


def set_user_session(user, session):
    session[SESSION_KEY] = user._meta.pk.value_to_string(user)
    session[BACKEND_SESSION_KEY] = 'django.contrib.auth.backends.ModelBackend'
    session[HASH_SESSION_KEY] = user.get_session_auth_hash()
