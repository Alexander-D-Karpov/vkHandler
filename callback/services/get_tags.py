from callback.models import Tag


def get_tags(body: list[str]) -> list[str]:
    all_tags = {}
    for tag in Tag.objects.all():
        all_tags[tag] = tag.tags.split(" ")
    tags = []
    for line in body:
        print(line)
        for word in line.split(' '):
            if word and word[0] == "#":
                for tag in all_tags:
                    if word[1:] in all_tags[tag]:
                        tags.append(tag)
    return tags
