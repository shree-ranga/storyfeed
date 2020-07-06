from django.urls import path
from .views import HomeView, TermsView, PrivacyView, CommunityGuidelinesView

urlpatterns = [
    path("", HomeView.as_view()),
    path("terms/", TermsView.as_view(), name="terms"),
    path("privacy/", PrivacyView.as_view(), name="privacy"),
    path(
        "community-guidelines/",
        CommunityGuidelinesView.as_view(),
        name="community_guidelines",
    ),
]
