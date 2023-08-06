import json as j
import re
from typing import List, Optional, Tuple

from tabulate import tabulate

from bpkio_cli.api.crudeApi import BroadpeakIoCrudeApi
from bpkio_cli.utils import pluck


def treat_list_objects(
    objects: List,
    select_fields: Optional[List[str]] = None,
    search: Optional[List[Tuple[str, str]]] = None,
    json: Optional[bool] = False,
):
    # Clean it up first
    objects = BroadpeakIoCrudeApi.strip_resource_decorations(objects)

    if search:
        for field, value in search:
            original_field = field

            # check that the field exist
            if field != "ANY":
                field_exists = any(o.get(field) for o in objects)
                if not (field_exists):
                    field = "#" + field
                    field_exists = any(o.get(field) for o in objects)

                if not (field_exists):
                    raise Exception(
                        f"Field '{original_field}' does not exist on this object"
                    )

            objects = [
                o
                for o in objects
                if (field in o and re.search(value, str(o[field]), flags=re.IGNORECASE))
                or (
                    field == "ANY"
                    and any(
                        re.search(value, str(o[k]), flags=re.IGNORECASE)
                        for k in o.keys()
                    )
                )
            ]

    if json:
        print(j.dumps(objects, indent=2))
        return

    # Extract the select_fields
    if select_fields:
        select_fields = " ".join(select_fields)  # type: ignore
        select_fields = re.split("\W+", select_fields)  # type: ignore

    data = pluck(objects, select_fields)
    print(tabulate(data, headers="keys"))
    return


def treat_single_object(
    object: List,
):
    object = BroadpeakIoCrudeApi.strip_resource_decorations(object)

    print(j.dumps(object, indent=2))
    return
