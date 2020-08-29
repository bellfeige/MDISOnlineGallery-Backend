from django.urls import path
from django.conf.urls import include, url
from rest_framework import routers
from .views import DigitalArtViewSet, RatingCommentViewSet, UserViewSet, UserProfileViewSet, CurrentUserView, \
    MDISMemberViewSet, CategoryViewSet, CartViewSet, OrderViewSet,MyDigitalArtViewSet

router = routers.DefaultRouter()
router.register("products", DigitalArtViewSet, basename='products')
router.register("my-products", MyDigitalArtViewSet, basename='my-products')
router.register("rating-comments", RatingCommentViewSet)
router.register("users", UserViewSet, basename='user')
router.register("my-profile", UserProfileViewSet, basename='my-profile')
router.register("mdis-members", MDISMemberViewSet, basename='mdis-members')
router.register("product-categories", CategoryViewSet)
router.register("cart", CartViewSet, basename='cart')
router.register("order", OrderViewSet, basename='order')

urlpatterns = [
    path("", include(router.urls)),
    path("me", CurrentUserView.as_view()),
]
