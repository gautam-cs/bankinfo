from rest_framework import serializers

from banks.models import Branches, Banks


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banks
        fields = '__all__'


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branches
        fields = '__all__'
