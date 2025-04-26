from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import BankBranchSerializer
from .models import Country, BankBranch


class BankBranchDetailsView(APIView):
    def get(self, request, swift_code, *args, **kwargs):
        if len(swift_code) != 11 and len(swift_code) != 8:
            return Response(
                { 'error': 'Incorrect length of swift code' },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            mainBranch = BankBranch.objects.get(swift_code=swift_code)

            data = {
                'address': mainBranch.bank_address,
                'bankName': mainBranch.bank_name,
                'countryISO2': mainBranch.country.ISO2,
                'countryName': mainBranch.country.country_name,
                'isHeadquarters': True if mainBranch.swift_code.endswith('XXX') else False,
                'swiftCode': mainBranch.swift_code,
            }

            if data['isHeadquarters']:
                data['branches'] = self.get_branches(swift_code)

            return Response(
                data,
                status=status.HTTP_200_OK,
            )
        except BankBranch.DoesNotExist:
            return Response(
                { 'error': 'Bank branch not found' },
                status=status.HTTP_404_NOT_FOUND,
            )

    def delete(self, request, swift_code, *args, **kwargs):
        if len(swift_code) != 11 and len(swift_code) != 8:
            return Response(
                { 'error': 'Incorrect length of swift code' },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            branch = BankBranch.objects.get(swift_code=swift_code)
            branch.delete()

            return Response(
                { 'message': 'Bank branch deleted successfully' },
                status=status.HTTP_200_OK,
            )
        except BankBranch.DoesNotExist:
            return Response(
                { 'error': 'Bank branch not found' },
                status=status.HTTP_404_NOT_FOUND,
            )

    def get_branches(self, swift_code):
        data = []

        branches = BankBranch.objects.filter(swift_code__startswith=swift_code[:7])

        for branch in branches:
            if branch.swift_code.endswith("XXX"): continue

            data.append({
                'address': branch.bank_address,
                'bankName': branch.bank_name,
                'countryISO2': branch.country.ISO2,
                'isHeadquarters': True if branch.swift_code.endswith('XXX') else False,
                'swiftCode': branch.swift_code,
            })

        return data


class CountryBankBranchesView(APIView):
    def get(self, request, countryISO2code, *args, **kwargs):
        try:
            country = Country.objects.get(ISO2=countryISO2code.upper())

            branches = BankBranch.objects.filter(country=country)

            data = {
                'countryISO2': country.ISO2,
                'countryName': country.country_name,
                'swiftCode': [],
            }

            for branch in branches:
                data['swiftCode'].append({
                    'address': branch.bank_address,
                    'bankName': branch.bank_name,
                    'countryISO2': branch.country.ISO2,
                    'isHeadquarters': True if branch.swift_code.endswith('XXX') else False,
                    'swiftCode': branch.swift_code,
                })

            return Response(
                data,
                status=status.HTTP_200_OK,
            )
        except BankBranch.DoesNotExist or Country.DoesNotExist:
            return Response(
                { 'error': 'No bank branches in that country' },
                status=status.HTTP_404_NOT_FOUND,
            )


class BankBranchCreateUpdateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = BankBranchSerializer(data=request.data)

        if serializer.is_valid():
            bank_branch = serializer.save()

            return Response(
                { 'message': 'Bank branch created/updated successfully.' },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

