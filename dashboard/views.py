from django.shortcuts import render, get_object_or_404
from .models import Post


def index(request):
    return render(request, 'dashboard/index.html')

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    session_key = f'viewed_post_{post.id}'

    if not request.session.get(session_key):
        post.views_count += 1
        post.save()

        request.session[session_key] = True
        request.session.set_expiry(86400)

    return render(request, 'blog/post_detail.html', {'post': post})