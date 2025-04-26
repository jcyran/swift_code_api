from rest_framework import serializers
from .models import Country, BankBranch

class BankBranchSerializer(serializers.Serializer):
    address = serializers.CharField(max_length=255)
    bankName = serializers.CharField(max_length=255)
    countryISO2 = serializers.CharField(max_length=2)
    countryName = serializers.CharField(max_length=255)
    isHeadquarter = serializers.BooleanField()
    swiftCode = serializers.CharField(max_length=11)

    def create(self, validated_data):
        country, _ = Country.objects.get_or_create(
            ISO2=validated_data['countryISO2'].upper(),
            defaults={ 'country_name': validated_data['countryName'].upper() },
        )

        if country.country_name != validated_data['countryName']:
            country.country_name = validated_data['countryName']
            country.save

        bankBranch, _ = BankBranch.objects.get_or_create(
            swift_code=validated_data['swiftCode'],
            defaults={
                'country': country,
                'bank_name': validated_data['bankName'],
                'bank_address': validated_data['address'],
            }
        )

        return bankBranch
