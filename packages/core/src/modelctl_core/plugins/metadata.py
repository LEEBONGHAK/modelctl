from pydantic import BaseModel


class PluginMetadata(BaseModel):
    """
    Common metadata for all modelctl plugins.
    """

    name: str

    version: str

    description: str | None = None

    author: str | None = None
