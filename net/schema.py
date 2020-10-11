import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User

from api.models import Comment, Post

class PostQL(DjangoObjectType):

    # comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ("id", "content", "timestamp", "author", "picture", "comments")
    
    #comments = graphene.String()

    @classmethod
    def resolve_comments(self, info, post):
        return Comments.objects.filter(post=self)

class CommentQL(DjangoObjectType):
    class Meta:
        model = Comment
        fields = ("id", "author", "post", "timestamp", "content")

class UserQL(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "email")

class Query(graphene.ObjectType):
    all_posts = graphene.List(PostQL)
    all_users = graphene.List(UserQL)
    all_comments = graphene.List(CommentQL)
    
    # comments_by_post = graphene.Field(CommentQL, name=graphene.String(required = True))

    post_by_id = graphene.Field(PostQL, id=graphene.Int(required=True))

    def resolve_all_posts(root, info):
        return Post.objects.select_related("author").all()
    
    def resolve_all_comments(root, info):
        return Comment.objects.select_related("author").all()

    def resolve_all_users(root, info):
        return User.objects.all()

    def resolve_post_by_id(root, info, id):
        try:
            return Post.objects.get(id=id)
        except Post.DoesNotExist:
            return None


    

schema = graphene.Schema(query=Query)
