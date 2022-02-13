def get_post_body(object: dict) -> list[str]:
    body = object["text"].split("\n")
    if "copy_history" in object:
        body += object["copy_history"][0]["text"].split("\n")

    return [x for x in body if x not in ["", " "]]
