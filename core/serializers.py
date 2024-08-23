from rest_framework import serializers
from .models import Pedido, PedidoVenda

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'


class PedidoVendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedidoVenda
        fields = '__all__'