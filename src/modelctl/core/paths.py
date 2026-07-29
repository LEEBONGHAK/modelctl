from pathlib import Path

from platformdirs import user_config_dir, user_data_dir


APP_NAME = "modelctl"


def config_dir() -> Path:
    """
    Configuration directory.
    """

    path = Path(
        user_config_dir(APP_NAME)
    )

    path.mkdir(
        parents=True,
        exist_ok=True
    )

    return path



def data_dir() -> Path:
    """
    Application data directory.
    """

    path = Path(
        user_data_dir(APP_NAME)
    )

    path.mkdir(
        parents=True,
        exist_ok=True
    )

    return path



def config_file() -> Path:

    return config_dir() / "config.toml"



def database_file() -> Path:

    return data_dir() / "modelctl.db"
