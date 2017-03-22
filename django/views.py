
from board.models import Post
from board.serializers import PostSerializer, PostDetailSerializer

from rest_framework import generics

from django.contrib.auth import authenticate

from board.permissions import IsOwnerOrReadOnly
from rest_framework import permissions

from board.serializers import UserSerializer, UserDetailSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from board.models import UserProfile
from django.contrib.auth.models import User


@api_view(['POST'])
def registration(request):
    if request.method == 'POST':
        data = request.data
        email = data['email']

        try:
            _ = User.objects.get(username=email)

            return Response({'msg': 'failed'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        except User.DoesNotExist:
            aa = User.objects.get(username=email)
            u = UserProfile()
            u.objects.get(user=aa)
            print(u)
            return Response({'msg': 'success'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def registration_confirmation(request):
    if request.method == 'POST':
        data = request.data
        email = data['email']
        code = data['code']

        print(email, code)
        authenticated_user = authenticate(username=email, password=code)

        if authenticated_user:
            user = UserProfile.objects.get(user=authenticated_user)
            user.is_confirmation = True
            user.save()
            return Response({'msg': 'success'}, status=status.HTTP_200_OK)
        else:
            return Response({'msg': 'failed'}, status=status.HTTP_401_UNAUTHORIZED)




class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    permissions_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    permissions_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)
    serializer_class = PostDetailSerializer


class UserList(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserDetailSerializer
    permissions_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)
