from rest_framework import serializers
from .models import Scrapedgame


class ScrapedgameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scrapedgame
        fields = '__all__'
