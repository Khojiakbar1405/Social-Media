from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from main import models
from . import serializers


from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.decorators import authentication_classes


class UserAPIView(APIView):
    def get(self, request, *args, **kwargs):
        q = request.GET.get('q')
        # way 1
        users = models.User.objects.all()
        if q:
            users.filter(
                Q(username__icontains=q)| 
                Q(first_name__iconatins=q)| 
                Q(last_name__iconatins=q)|
                Q(email__icontains=q)
                )
        # way 2
        # if q:
        #     users = models.User.objects.filter(
        #         Q(username__icontains=q)| 
        #         Q(first_name__iconatins=q)| 
        #         Q(last_name__iconatins=q)|
        #         Q(email__icontains=q)
        #     )
        # else:
        #     users = models.User.objects.all()

        serializer = serializers.UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk, *args, **kwargs):
        try:
            user = request.user
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        try:
            user = request.user
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class UserRelationAPIView(APIView):

    def get(self, request, *args, **kwargs):
        user = request.user
        following = models.UserReletion.objects.filter(from_user=user)
        follower = models.UserReletion.objects.filter(to_user=user)
        following_ser = serializers.FollowingSerializer(following, many=True)
        follower_ser = serializers.FollowerSerializer(follower, many=True)
        data = {
            'following':following_ser.data,
            'follower':follower_ser.data,
        }
        return Response(data)


    def post(self, request, *args, **kwargs):
        try:
            from_user = request.user
            to_user = request.data['to_user']
            models.UserReletion.objects.create(from_user=from_user, to_user=to_user)
            return Response(status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        try:
            to_user = models.User.objects.get(pk=pk)
            reletion = models.UserReletion.objects.get(
                from_user=request.user,
                to_user = to_user
                )
            reletion.delete()
            return Response(status=status.HTTP_200_OK)
        except models.UserReletion.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    
class ChatAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = serializers.ChatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None, format=None):
        user = request.user
        chats = models.Chat.objects.filter(users=user)
        chats_ser = serializers.ChatListSerializer(chats)
        return Response(chats_ser.data)
        # try:
        #     instance = models.Chat.objects.get(pk=pk)
        # except models.Chat.DoesNotExist:
        #     return Response({"message": "Object not found"}, status=status.HTTP_404_NOT_FOUND)

        # serializer = serializers.ChatSerializer(instance)
        # return Response(serializer.data)

    def delete(self, request, pk, *args, **kwargs):
        try:
            chat = models.Chat.objects.get(pk=pk)
        except models.Chat.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        chat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class MassageAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = serializers.MassageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, *args, **kwargs):
        try:
            massage = models.Message.objects.get(pk=pk)
            assert massage.author == request.user
        except models.Message.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.MassageSerializer(massage, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        try:
            massage = models.Message.objects.get(pk=pk)
            assert massage.author == request.user
        except models.Message.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        massage.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

@api_view
def following(request, pk):
    user = models.User.objects.get(pk=pk)
    user_reletion = models.UserReletion.objects.filter(from_user=user)
    serializer_data = serializers.FollowingSerializer(user_reletion, many=True)
    return serializer_data.data

@api_view
def follower(request, pk):
    user = models.User.objects.get(pk=pk)
    user_reletion = models.UserReletion.objects.filter(to_user=user)
    serializer_data = serializers.FollowerSerializer(user_reletion, many=True)
    return serializer_data.data


class PostView(APIView):
    @authentication_classes([SessionAuthentication, BasicAuthentication])
    def get(self, request, *args, **kwarg):
        post = models.Post.objects.filter(author = request.user)
        post_ser = serializers.PostSerializer(post, many = True)
        return Response(post_ser.data)
    

    @authentication_classes([SessionAuthentication, BasicAuthentication])
    def put(self, request, id, *args, **kwargs):
        post = models.Post.objects.filter(author = request.user).get(id = id)
        if request.data['title']:
            post.title = request.data['title']
        if request.data['body']:
            post.title = request.data['body']
        post.save()
        post_ser = serializers.PostSerializer(post)
        return Response(post_ser.data)
    

    def delete(self, request, id, *args, **kwargs):
        post = models.Post.objects.filter(author=request.user).get(id = id)
        post.delete()
        return Response({'success':'post has been deleted'})
    
@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def filter_post(request):
    search = request.data['search']
    post = models.Post.objects.filter(author = request.user)
    post.filter(Q(title__icontains = search) | Q(body__icontains = search))
    post_ser = serializers.PostSerializer(post, many = True)
    return Response (post_ser.data)



class CommentView(APIView):
    def get(self, request, id, *args, **kwargs):
        post = models.Post.objects.get(id=id)
        comment = models.Comment.objects.filter(post = post).order_by('-date')
        comment_ser = serializers.CommentSerializer(comment, many = True)
        return Response(comment_ser.data)
    

    @authentication_classes([SessionAuthentication, BasicAuthentication])
    def post(self, request, id, *args, **kwargs):
        if request.data.get('reply'):
            reply = models.Comment.objects.get(id = request['reply_id'])
            comment = models.Comment.objects.create(
                author = request.user,
                post = models.Post.objects.get(id=id),
                text = request.data['text'],
                reply = reply
            )
        else:
            comment = models.Comment.objects.create(
                author = request.user,
                post = models.Post.objects.get(id=id),
                text = request.data['text'],
            )
        comment_ser = serializers.CommentSerializer(comment)
        return Response({'comment':comment_ser.data})
    

    @authentication_classes([SessionAuthentication, BasicAuthentication])
    def put(self, request, id, *args, **kwargs):
        comment = models.Comment.objects.filter(author=request.user).get(id=id)
        comment.text = request.data['text']
        comment.save()
        comment_ser = serializers.CommentSerializer(comment)
        return Response({'comment': comment_ser.data})

    @authentication_classes([SessionAuthentication, BasicAuthentication])
    def delete(self, request, id, *args, **kwargs):
        comment = models.Comment.objects.filter(author = request.user).get(id = id)
        comment.delete()
        return Response({'success':'comment has been deleted'})

