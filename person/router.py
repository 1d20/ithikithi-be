from rest_framework import routers
from person import views


router = routers.DefaultRouter()
router.register(r'person', views.PersonViewSet)
