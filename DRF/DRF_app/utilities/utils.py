from DRF_app.customs.authentication import create_refresh_token,decode_refresh_token,create_access_token
def get_tokens_for_user(user):
    # refresh = RefreshToken.for_user(user)
    # access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)
    id = decode_refresh_token(refresh_token)
    refresh_access_token = create_access_token(user.id)

    return {
        "refresh": refresh_token,
        "access": refresh_access_token,
    }
