from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import BankBranch, Country
from .serializers import BankBranchSerializer
from .utils.swift_code import *


class BankBranchDetailsView(APIView):
    def get(self, request, swift_code, *args, **kwargs):
        if not is_valid_length_swift(swift_code):
            return Response(
                {"error": "Incorrect length of swift code."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            swift_code = normalize_swift_code(swift_code)

            mainBranch = BankBranch.objects.get(swift_code=swift_code)

            data = {
                "address": mainBranch.bank_address,
                "bankName": mainBranch.bank_name,
                "countryISO2": mainBranch.country.ISO2,
                "countryName": mainBranch.country.country_name,
                "isHeadquarter": is_headquarter_swift(mainBranch.swift_code),
                "swiftCode": mainBranch.swift_code,
            }

            if data["isHeadquarter"]:
                result = get_bank_branches_swift(swift_code)

                if "error" in result:
                    return Response(
                        data=result[0]["error"],
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )
                data["branches"] = result
            return Response(
                data,
                status=status.HTTP_200_OK,
            )
        except BankBranch.DoesNotExist:
            return Response(
                {"error": "Bank branch not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

    def delete(self, request, swift_code, *args, **kwargs):
        if not is_valid_length_swift(swift_code):
            return Response(
                {"error": "Incorrect length of swift code."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            swift_code = normalize_swift_code(swift_code)

            branch = BankBranch.objects.get(swift_code=swift_code)
            branch.delete()

            return Response(
                {"message": "Bank branch deleted successfully."},
                status=status.HTTP_200_OK,
            )
        except BankBranch.DoesNotExist:
            return Response(
                {"error": "Bank branch not found."},
                status=status.HTTP_404_NOT_FOUND,
            )


class CountryBankBranchesView(APIView):
    def get(self, request, countryISO2code, *args, **kwargs):
        if len(countryISO2code) != 2:
            return Response(
                {"error": "ISO2 always has exactly 2 letters."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            country = Country.objects.get(
                ISO2=countryISO2code.upper()
            )  # iso2 is only stored in uppercase, you can input lowercase

            branches = BankBranch.objects.filter(country=country)

            data = {
                "countryISO2": country.ISO2,
                "countryName": country.country_name,
                "swiftCodes": [],
            }

            for branch in branches:
                data["swiftCodes"].append(
                    {
                        "address": branch.bank_address,
                        "bankName": branch.bank_name,
                        "countryISO2": branch.country.ISO2,
                        "isHeadquarter": is_headquarter_swift(branch.swift_code),
                        "swiftCode": branch.swift_code,
                    }
                )

            return Response(
                data,
                status=status.HTTP_200_OK,
            )
        except Country.DoesNotExist:
            return Response(
                {"error": f"Couldn't find country with ISO2 = {countryISO2code}."},
                status=status.HTTP_404_NOT_FOUND,
            )


class BankBranchCreateUpdateView(APIView):
    def post(self, request, *args, **kwargs):
        required_fields = {
            "address",
            "bankName",
            "countryISO2",
            "countryName",
            "isHeadquarter",
            "swiftCode",
        }

        if not all(field in request.data for field in required_fields):
            return Response(
                {"error": "Incorrect json document."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = BankBranchSerializer(data=request.data)

        if not serializer.is_valid():
            error_response = serializer.get_errors()

            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(
            {"message": "Bank branch created successfully."},
            status=status.HTTP_201_CREATED,
        )
