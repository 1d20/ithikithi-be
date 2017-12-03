from person import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'person', views.PersonViewSet)
router.register(r'authenticate', views.AuthenticationViewSet, base_name='auth')