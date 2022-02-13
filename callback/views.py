from django.http import HttpResponse
from rest_framework.response import Response

from .models import Post
from .serializers import PostSerializer
from rest_framework import mixins
from rest_framework import generics
from secrets import compare_digest

from .services.prepare_post import prepare_post

secret = "8a1442ec76a9571c8f58e3e24616d9440"


class PostCallback(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def post(self, request, *args, **kwargs):
        if request.data['type'] == "confirmation":
            return HttpResponse('dafbfb3c', content_type="application/json")

        elif request.data['type'] == "wall_post_new" and compare_digest(request.data['secret'], secret) \
                and not Post.objects.filter(event_id=request.data['event_id']).exists():
            prepare_post(request.data)
            return Response("OK")
        return Response("event already exists or key is not correct")
