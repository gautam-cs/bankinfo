from django.contrib.auth.models import User, Group
from rest_framework import serializers

from banks.models import Branches


class BankSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('bank_name', 'bank_id')


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branches
        fields = '__all__'
