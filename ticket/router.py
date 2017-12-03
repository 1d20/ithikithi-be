from ticket import views
from rest_framework import routers


router = routers.DefaultRouter()

router.register(r'ticket', views.TicketViewSet)
