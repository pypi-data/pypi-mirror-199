import re


def query_sort(sort, direction, schema):
    """
    Validation and parameterization of the provided sort
    :param sort: {str}
    :param direction: {str}
    :param schema: {dict} Schema whose keys will be compared against
    :return: parameterized sort
    """
    # Validate that the sorting is operating on a valid movie field, and directionality is reasonable
    if sort and sort not in schema or direction not in ("asc", "dsc"):
        raise ValueError(
            'Sorts must be applied to a movie field, and expect a direction of "asc" or "dsc"'
        )
    elif sort:
        return f"sort={sort}:{direction}"
    else:
        return ""


def query_filter(filter, schema):
    """
    Validate for the filter against schema fields, opportunity to expand on known filter options
    :param filter: {str} Filter to be applied to search.  Must match a Movie field,
        and supports (non)match, include/exclude, exists/does not exist, regex,
        and greater than/less than/equal to comparisons
    :param schema: {dict} Schema whose keys will be compared against
    :return: filter to be applied
    """
    # Validate that the filter is operating on a valid movie field; skipping operator validity
    # for brevity's sake; in general this should just return an empty set which is a reasonable response
    if filter and (re.findall(r"^[a-zA-Z]+", filter) or [""])[0] not in schema:
        raise ValueError("Sorts must be applied to a valid movie field")
    return filter
