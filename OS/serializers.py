from rest_framework import serializers
from .models import OrdemServico

class OSSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrdemServico
        fields = '__all__'