from ninja import Schema, UploadedFile, File
from typing import List
from pydantic import Field


class CommentOwner(Schema):
    id: int
    username: str


class PostOwner(Schema):
    id: int
    username: str


class PostImages(Schema):
    id: int
    image: str


class PostSchemaIn(Schema):
    title: str
    content: str
    images: List[UploadedFile] = File(default=None)


class CommentSchema(Schema):
    id: int
    comment: str


class CommentParent(CommentSchema):
    commenter: CommentOwner
    parent_id: int = None


class PostOut(Schema):
    id: int
    owner: PostOwner
    title: str
    content: str
    comments: List[CommentParent] = Field(alias='postcomment_set')
    images: List[PostImages] = Field(alias='postimages_set')