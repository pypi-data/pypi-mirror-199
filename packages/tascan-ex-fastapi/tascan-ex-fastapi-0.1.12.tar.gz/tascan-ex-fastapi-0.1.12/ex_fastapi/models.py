from ex_fastapi.settings import Databases, get_settings


match Databases(get_settings('db_name')):
    case Databases.tortoise:
        from ex_fastapi.contrib.tortoise.models import \
            BaseModel, default_of, max_len_of,\
            ContentType,\
            Permission, PermissionGroup, PermissionMixin,\
            BaseUser, UserWithPermissions, BaseTempCode
    case _:
        raise ImportError('No database chosen')

__all__ = [
    BaseModel, default_of, max_len_of,
    ContentType,
    Permission, PermissionGroup, PermissionMixin,
    BaseUser, UserWithPermissions, BaseTempCode
]
