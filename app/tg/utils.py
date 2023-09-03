def parser_callback_data(data: str):
    if not data:
        raise ValueError("data empty")

    p1 = data.split("?")
    if len(p1) > 1:
        raw_path, raw_params = p1
    else:
        raw_path, raw_params = *p1, None

    path: list = raw_path.split("/")
    while "" in path:
        path.remove("")

    params = dict([p.split("=") for p in raw_params.split("&")]) if raw_params else {}
    return path, params
