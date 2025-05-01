from rest_framework import serializers

from .models import BankBranch, Country
from .utils.swift_code import *


class BankBranchSerializer(serializers.Serializer):
    address = serializers.CharField(max_length=255, required=True)
    bankName = serializers.CharField(max_length=255, required=True)
    countryISO2 = serializers.CharField(max_length=2, required=True)
    countryName = serializers.CharField(max_length=255, required=True)
    isHeadquarter = serializers.BooleanField(required=True)
    swiftCode = serializers.CharField(max_length=11, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._errors = {}

    def validate_countryISO2(self, value):
        if len(value) != 2 or not value.isalpha():
            self._errors["countryISO2"] = "Invalid ISO2 code."
            raise serializers.ValidationError("Invalid ISO2 code.")

        return value.upper()

    def validate_swiftCode(self, value):
        if not is_valid_length_swift(value):
            self._errors["swiftCode"] = "Invalid swift code."
            raise serializers.ValidationError("Invalid swift code.")

        return value

    def validate(self, data):
        is_hq = data.get("isHeadquarter")
        swift = data.get("swiftCode")

        if is_hq and not is_headquarter_swift(swift):
            self._errors["swiftCode"] = (
                'Headquarters must have swift code ending with "XXX".'
            )
            raise serializers.ValidationError(
                {"error": 'Headquarters must have swift code ending with "XXX".'}
            )

        data["countryName"] = data["countryName"].upper()

        if self._errors:
            raise serializers.ValidationError(self._errors)

        return data

    def get_errors(self):
        if not self._errors:
            return None

        if len(self._errors) == 1:
            return {"error": next(iter(self._errors.values()))}

        combined = "; ".join(f"{field}: {msg}" for field, msg in self._errors.items())

        return {"error": combined}

    def create(self, validated_data):
        data = validated_data.copy()

        data["swiftCode"] = normalize_swift_code(data["swiftCode"])

        country, _ = Country.objects.get_or_create(
            ISO2=data["countryISO2"].upper(),
            defaults={"country_name": data["countryName"].upper()},
        )

        country.save()

        bankBranch, _ = BankBranch.objects.get_or_create(
            swift_code=data["swiftCode"],
            defaults={
                "country": country,
                "bank_name": data["bankName"],
                "bank_address": data["address"],
            },
        )

        return bankBranch
