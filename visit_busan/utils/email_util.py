import random

from account.cache.save_authorized_code import save_authorized_code

RANDOM_CONDE_LENGTH = 4


def send_sign_up_email(email):
    authorized_code = random.randrange(1000, 10000)

    return save_authorized_code(authorized_code, email)
