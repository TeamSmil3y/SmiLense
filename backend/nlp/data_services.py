from db_init import *


def check_dependency_cache(name: str, version: str) -> bool:
    """
    Checks whether a cache entry for the package exists

    :param name: package name
    :param version: package version
    :return: true or false (duh)
    """

    with db_engine.connect() as connection:
        res = connection.execute(packages.select().where(and_(packages.c.name == name, packages.c.version == version)))

    if len(res.all()) > 0:
        return True
    return False

def check_license_cache(hash: str) -> bool:
    """
    Checks whether a cache entry for the license exists

    :param hash: license hash
    :return: true or false (duh)
    """

    with db_engine.connect() as connection:
        res = connection.execute(licenses.select().where(licenses.c.hash == hash))

    if len(res.all()) > 0:
        return True
    return False


def get_cached_properties(name: str, version: str) -> dict:
    """
    Grabs properties for license of package

    :param name: package name
    :param version: package version
    :return: license properties
    """
    with db_engine.connect() as connection:
        res = connection.execute(
            sql.select(
                packages.c.name,
                packages.c.version,

                licenses.c.commercial_use,
                licenses.c.open_source,
                licenses.c.attribution,
                licenses.c.redistribution,
                licenses.c.profit,
                licenses.c.free,
                licenses.c.additional,

            ).where(
                and_(
                    packages.c.name == name,
                    packages.c.version == version,
                    packages.c.hash == licenses.c.hash,
                )
            )
        )

    return {
        "commercial_use": res[2],
        "open_source": res[3],
        "attribution": res[4],
        "redistribution": res[5],
        "profit": res[6],
        "free": res[7],
        "additional": res[8]
    }


def write_cache(name: str, version: str, hash: str, properties: dict) -> bool:
    """
    Writes license properties of package to cache

    :param name: package name
    :param version: package version
    :param hash: license hash
    :param properties: license properties
    :return: true or false indicating whether write was successful
    """

    def write_package(name: str, version: str, hash: str):
        with db_engine.connect() as connection:
            res = connection.execute(
                sql.insert(
                    packages
                ).values(
                    name=name,
                    hash=hash,
                    version=version,
                )
            )
            connection.commit()

    def write_license(hash: str, properties: dict):
        with db_engine.connect() as connection:
            res = connection.execute(
                sql.insert(
                    licenses
                ).values(
                    hash=hash,
                    **properties
                )
            )
            connection.commit()



