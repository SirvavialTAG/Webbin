from rest_framework import viewsets, generics
from .models import Brands, Cars
from .serializers import BrandSerializer, CarSerializer
from django_filters import rest_framework as filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import JSONRenderer
import requests

class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Brands.objects.all() # Получаем все данные из таблицы Brands
    serializer_class = BrandSerializer # Сериализатор для JSON
    renderer_classes = [JSONRenderer]


class Cars_filter(filters.FilterSet):
    year_from = filters.NumberFilter(field_name='year', lookup_expr='gte')
    year_to = filters.NumberFilter(field_name='year', lookup_expr='lte')
    drive = filters.CharFilter(field_name='drive')
    drive = filters.CharFilter(field_name='drive')
    transmission = filters.CharFilter(field_name='transmission')
    color = filters.CharFilter(method='color_filter')


    ordering = filters.CharFilter(method='sorting') # Сортировка

    class Meta:
        model = Cars
        fields = ['year_from', 'year_to', 'drive', 'transmission', 'color']

    sort_dict = {
        'price_asc': 'price',
        'price_desc': '-price',
        'year_asc': 'year',
        'year_desc': '-year',
        'mileage_asc': 'mileage',
        'mileage_desc': '-mileage',
        'volume_asc': 'engine_volume',
        'volume_desc': '-engine_volume',
    }

    def sorting(self, queryset, sort_val):
        """ Ищет параметры сортировки в словаре sort_dict и сортирует по ним. """

        if sort_val in self.sort_dict:
            order_by = self.sort_dict[sort_val]
            return queryset.order_by(order_by)
        return queryset

    def get_sort_fields(self):
        """ Возвращает ключи словаря sort_dict. """

        return list(self.sort_dict.keys())

    def get_colors_dict(self):
        """Возвращает словарь цветов для фильтрации."""

        colors_dict = {
            'red': 'Красный',
            'blue': 'Синий',
            'green': 'Зеленый',
            'white': 'Белый',
            'pink': 'Розовый',
            'silver': 'Серебряный',
            'gray': 'Серый',
            'beige': 'Бежевый',
            'vinous': 'Бордовый',
            'yellow': 'Желтый',
            'golden': 'Золотой',
            'orange': 'Оранжевый',
            'brown': 'Коричневый',
            'purple': 'Фиолетовый',
        }
        return colors_dict

    def color_filter(self, queryset, color_val):
        """Ищет необходимый цвет и фильтрует по нему."""

        if color_val in self.get_colors_dict():
            return queryset.filter(color=color_val)
        return queryset


class CarsCatalog(generics.ListAPIView):
    queryset = Cars.objects.all()
    serializer_class = CarSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = Cars_filter
    pagination_class = PageNumberPagination
    renderer_classes = [JSONRenderer]


class CarsModel(generics.ListAPIView):
  serializer_class = CarSerializer

  def get_queryset(self):
    brandID = self.kwargs.get('brand__id')

    if not brandID:
      return Cars.objects.none()

    return Cars.objects.filter(brand__id=brandID).distinct('model').order_by('model')