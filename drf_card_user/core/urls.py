from rest_framework.routers import SimpleRouter

from cards.views import CardViewSet
from users.views import UserViewSet

router = SimpleRouter(trailing_slash=False)

router.register(r'users', UserViewSet, basename="user")
router.register(r'cards', CardViewSet, basename="card")

urlpatterns = router.urls
