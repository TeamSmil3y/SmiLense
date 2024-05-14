from extract_key_points import *
from db_init import *
import os

directory = "/Users/timruppert/Downloads/scancode-licensedb-main/docs"

with db_engine.connect() as connection:
    for filename in os.listdir(directory):
        if filename.startswith("."): continue
        with open(directory + "/" + filename, "r") as file:

            f = file.read().split("---\n")
            d = {i.split(":")[0]: ":".join(i.split(":")[1:]) for i in f[1].split("\n") if i}
            print(d)

            if len(connection.execute(sql.select(licenses).where(licenses.columns.name == d["name"])).all()) > 0:
                continue

            raw = "\n".join(f[2:])
            url_key = None
            for key in d.keys():
                if "url" in key:
                    url_key = key
                    break


            key_parameters = ", ".join(extract_key_points(raw))

            print(key_parameters)

            connection.execute(sql.insert(licenses).values(key=d["key"], name=d["name"], short_name=d["short_name"], category=(d["category"] if "category" in d else None), url=d[url_key] if url_key else None, raw=raw, key_parameters=key_parameters))
        connection.commit()
