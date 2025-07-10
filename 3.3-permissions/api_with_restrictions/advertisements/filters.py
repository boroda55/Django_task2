from django.contrib.auth.models import User
from django_filters import rest_framework as filters, DateFromToRangeFilter
from rest_framework import generics

from advertisements.models import Advertisement
from advertisements.serializers import AdvertisementSerializer


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""

    # TODO: задайте требуемые фильтры
    created_at = DateFromToRangeFilter()
    creator = filters.ModelChoiceFilter(queryset=User.objects.all())

    class Meta:
        model = Advertisement
        fields = ('created_at')


class AdvertisementList(generics.ListAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AdvertisementFilter

