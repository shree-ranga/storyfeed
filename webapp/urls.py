from django.urls import path
from .views import HomeView, TermsView, PrivacyView

urlpatterns = [
    path("", HomeView.as_view()),
    path("terms/", TermsView.as_view(), name="terms-storyfeed"),
    path("privacy/", PrivacyView.as_view(), name="privacy-storyfeed"),
]
