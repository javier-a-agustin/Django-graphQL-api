import graphene
import graphql_jwt
from graphene_django import DjangoObjectType
# from django.contrib.auth.models import User

from api.models import Comment, Post
from django.contrib.auth import get_user_model

User = get_user_model()

class PostQL(DjangoObjectType):

    # comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ("id", "content", "timestamp", "author", "picture", "comments")

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
    post_by_id = graphene.Field(PostQL, id=graphene.Int(required=True))
    comment_by_id = graphene.Field(CommentQL, id=graphene.Int(required=True))
    user_by_username = graphene.Field(UserQL, username=graphene.String(required=True))

    me = graphene.Field(UserQL)

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
    
    def resolve_comment_by_id(root, info, id):
        try:
            return Comment.objects.get(id=id)
        except Comment.DoesNotExist:
            return None
    
    def resolve_user_by_username(root, info, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None

    def resolve_me(root, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')      
        return user

class CreateUser(graphene.Mutation):
    user = graphene.Field(UserQL)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=False)

    def mutate(self, info, username, password, email):
        user = User(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)

class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    create_user = CreateUser.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
