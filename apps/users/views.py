# -*- coding: UTF-8 -*-
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.mixins import CreateModelMixin
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.response import Response
from rest_framework import status
from random import choice
from rest_framework import permissions
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler
from rest_framework.views import APIView

from apps.users.serializers import UserRegisterSerializer, UserDetailSerializer
from rest_framework_jwt.utils import jwt_decode_handler

import json

User = get_user_model()

class UserViewset(CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    用户
    """
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    #动态配置返回的用户信息
    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        elif self.action == "create":
            return UserRegisterSerializer
        return UserDetailSerializer

    # permission_classes = (permissions.IsAuthenticated, )
    #重载获取权限的函数，动态配置权限，注册不需要权限
    def get_permissions(self):
        if self.action == "retrieve":
            return [permissions.IsAuthenticated()]
        elif self.action == "create":
            return []
        return []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def get_object(self):
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()
#
#
# class UserDetail(APIView):
#
#     def get_object(self, request, *args, **kwargs):
#
#         username = jwt_decode_handler(token)
#
#         try:
#             return UserDetailSerializer.objects.get(username=username)
#         except Exception as e:
#             pass
#
#     def get(self, request, *args, **kwargs):
#         username = jwt_decode_handler(token)
#
#         snippet = self.get_object(pk)
#         serializer = SnippetSerializer(snippet)
#         return Response(serializer.data)
#
#
#
#         serializer = self.get_serializer(instance)
#         return Response(serializer.data)