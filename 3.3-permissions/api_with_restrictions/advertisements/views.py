from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from advertisements.models import Advertisement
from advertisements.permissions import IsOwnerOrReadOnly
from advertisements.serializers import AdvertisementSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    # TODO: настройте ViewSet, укажите атрибуты для кверисета,
    #   сериализаторов и фильтров

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            if self.request.user.is_superuser:
                return []
            else:
                return [IsAuthenticated(), IsOwnerOrReadOnly()]
        return []

    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = (Advertisement.objects.filter(creator=self.request.user) |
                        Advertisement.objects.filter(status='OPEN')
                        )
            return queryset
        return super().get_queryset().filter(status='OPEN')