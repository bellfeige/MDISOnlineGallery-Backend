from django.contrib.auth.hashers import make_password


def hashed_password(raw_password):
    return make_password(raw_password)


# plain_text = 'Aa111111'
# password = make_password(plain_text)
# print(password)
