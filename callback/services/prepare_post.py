from callback.models import Post, PostTag
from callback.services.clean_post import clean_post
from callback.services.get_tags import get_tags
from callback.services.get_post_body import get_post_body
from callback.services.send_at_all import send_at_all


def prepare_post(post: dict) -> None:
    body = get_post_body(post["object"])
    tags = get_tags(body)
    c_body = clean_post(body)
    url = f"https://vk.com/wall-{post['group_id']}_{post['object']['id']}"
    o_post = Post.objects.create(text=c_body, event_id=post["event_id"], link=url)
    for tag in tags:
        PostTag.objects.create(post=o_post, tag=tag)
    send_at_all(o_post)