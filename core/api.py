from typing import List
from django.shortcuts import get_object_or_404
from ninja import Router, File, Form
from ninja.files import UploadedFile
from .schemas import PostOut, PostSchemaIn
from .models import Post, PostImages, PostComment
from auth.jwt import AuthBearer


router = Router()


@router.post("/create-post/", auth=AuthBearer())
def create_post(request, title: str = Form(...), content: str = Form(...), files: List[UploadedFile] = File(default=None)):
    post_create = Post.objects.create(owner=request.auth, title=title, content=content)
    if files:
        for f in files:
            images = PostImages.objects.create(post=post_create, image=f)
        return f'Post created'
    return 'Post Created'


@router.post('/comment/{post_id}', auth=AuthBearer())
def post_comment(request, post_id: int, comments: str, parent_id: int = None):
    post = get_object_or_404(Post, id=post_id)
    if parent_id:
        comment = PostComment.objects.create(post=post, user=request.auth, comment=comments, parent_id=parent_id)
        return f'Reply added to comment {parent_id}'
    else:
        comment = PostComment.objects.create(post=post, user=request.auth, comment=comments)
        return f'Comment add to post {post.id}'


@router.get('/posts/', response=List[PostOut], auth=AuthBearer())
def get_all_posts(request):
    qs = Post.objects.all()
    return qs


@router.get('/post/{post_id}', response=PostOut, auth=AuthBearer())
def get_post(request, post_id: int):
    qs = get_object_or_404(Post, id=post_id)
    return qs


@router.delete('/delete/post/{post_id}/', auth=AuthBearer())
def delete_post(request, post_id: int):
    post = get_object_or_404(Post, id=post_id)
    if post.owner == request.auth:
        post.delete()
        return f'Post {post_id} deleted'
    else:
        return f'Unauthorized'


@router.get('/myposts/', response=List[PostOut], auth=AuthBearer())
def get_my_posts(request):
    qs = Post.objects.filter(owner=request.auth)
    return qs



