import time

from repository import *
from exceptions.exceptions import *
from configurations.database_config import redis_client, database


def authenticate(email: str, password: str) -> str:
    for _ in range(3):
        try:
            if not validate_email(email):
                raise ValueError("Format de email invalid.")

            if not validate_password(password):
                raise ValueError(
                    "Parola trebuie sa fie de minim 8 caractere si sa aiba macar o litera mare, "
                    "o litera mica, o cifra si un caracter special."
                )

            if database.is_closed():
                database.connect()

            user = get_user_by_email(email)
            print(f"User: {user}")

            if user is None:
                raise UserNotFoundException(f"Nu a fost gasit niciun utilizator cu emailul {email}.")

            is_valid = check_credentials(password, user)
            if not is_valid:
                raise InvalidCredentialsException("Date de conectare invalide.")

            return generate_token(user)
        finally:
            if not database.is_closed():
                database.close()
            time.sleep(1)

def validate(token: str) -> (str, str):

    payload, error_message = decode_token(token)

    if error_message is not None:
        raise InvalidOrExpiredTokenException(error_message)

    sub, role = payload["sub"], payload["role"]

    return sub, role

def destroy(token: str) -> bool:

    if redis_client.exists(token):
        return False

    redis_client.set(token, "destroyed", ex=3600 * 72)

    return True