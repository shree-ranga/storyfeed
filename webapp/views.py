from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status


class HomeView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "webapp/home.html"

    def get(self, request):
        return Response({})


class TermsView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "webapp/terms.html"

    def get(self, request):
        return Response({})


class PrivacyView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "webapp/privacy.html"

    def get(self, request):
        return Response({})


class CommunityGuidelinesView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "webapp/guidelines.html"

    def get(self, request):
        return Response({})
