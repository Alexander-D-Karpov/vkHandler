def get_post_body(object: dict) -> list[str]:
    if "copy_history" in object:
        body = object["copy_history"]["text"]
    else:
        body = object["text"]

    return [x for x in body.split("\n") if x]