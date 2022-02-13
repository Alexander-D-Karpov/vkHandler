def clean_post(body: list[str]) -> str:
    data = []
    for line in body:
        l = " ".join(filter(lambda x: x and x[0] != "#", line.split(" ")))
        if l:
            data.append(l)
    return "\n".join(data)
