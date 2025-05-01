from rest_framework.test import APITestCase

from api.models import BankBranch, Country


class SetUpTest(APITestCase):
    def setUp(self):
        self.country = Country.objects.create(ISO2="PL", country_name="POLAND")
        self.headquarter = BankBranch.objects.create(
            swift_code="ABCDEF12XXX",
            country=self.country,
            bank_name="TEST HEADQUARTER",
            bank_address="123 Main St",
        )
        self.branch = BankBranch.objects.create(
            swift_code="ABCDEF12345",
            country=self.country,
            bank_name="TEST BRANCH",
            bank_address="345 Common St",
        )

        self.headquarter_data = {
            "address": "123 Main St",
            "bankName": "TEST HEADQUARTER",
            "countryISO2": "PL",
            "countryName": "POLAND",
            "isHeadquarter": True,
            "swiftCode": "ABCDEF12XXX",
        }

        self.branch_data = {
            "address": "345 Common St",
            "bankName": "TEST BRANCH",
            "countryISO2": "PL",
            "countryName": "POLAND",
            "isHeadquarter": False,
            "swiftCode": "ABCDEF12345",
        }

        return super().setUp()

    def tearDown(self):
        return super().tearDown()
