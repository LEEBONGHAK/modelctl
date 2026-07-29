import keyring


SERVICE_NAME = "modelctl"



def set_secret(
    name: str,
    value: str
):

    keyring.set_password(
        SERVICE_NAME,
        name,
        value
    )



def get_secret(
    name: str
):

    return keyring.get_password(
        SERVICE_NAME,
        name
    )



def delete_secret(
    name: str
):

    keyring.delete_password(
        SERVICE_NAME,
        name
    )
