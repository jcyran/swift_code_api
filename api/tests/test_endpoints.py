from pydoc import resolve

from django.http import response

from api.models import BankBranch, Country
from api.utils import swift_code

from .test_setup import SetUpTest


# Tests for the first endpoint (/v1/swift-codes/{swift-code})
class SwiftCodeBankDetailsTest(SetUpTest):
    def test_get_branch_correct_data(self):
        response = self.client.get("/v1/swift-codes/ABCDEF12345")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, self.branch_data)

    def test_get_headquarter_len11_correct_data(self):
        response = self.client.get("/v1/swift-codes/ABCDEF12XXX")

        self.assertEqual(response.status_code, 200)

        self.branch_data.pop("countryName")
        self.headquarter_data["branches"] = []
        self.headquarter_data["branches"].append(self.branch_data)

        self.assertEqual(response.data, self.headquarter_data)

    def test_get_headquarter_len8_correct_data(self):
        response = self.client.get("/v1/swift-codes/ABCDEF12")

        self.assertEqual(response.status_code, 200)

        self.branch_data.pop("countryName")
        self.headquarter_data["branches"] = []
        self.headquarter_data["branches"].append(self.branch_data)

        self.assertEqual(response.data, self.headquarter_data)

    def test_swift_incorrect_length(self):
        response = self.client.get("/v1/swift-codes/ABCDEF1234")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "Incorrect length of swift code.")

    def test_swift_code_doesnt_exist(self):
        response = self.client.get("/v1/swift-codes/00000000000")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["error"], "Bank branch not found.")

    def test_empty_swift_code(self):
        response = self.client.get("/v1/swift-codes/")

        self.assertEqual(response.status_code, 404)


# Tests for the second endpoint (/v1/swift-codes/country/{ISO2-code})
class CountryBankDetailsTest(SetUpTest):
    def test_iso2_valid_uppercase(self):
        response = self.client.get("/v1/swift-codes/country/PL")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["countryName"], "POLAND")

        self.branch_data.pop("countryName")
        self.headquarter_data.pop("countryName")

        self.assertEqual(response.data["swiftCodes"][0], self.headquarter_data)
        self.assertEqual(response.data["swiftCodes"][1], self.branch_data)

    def test_iso2_valid_lowercase(self):
        response = self.client.get("/v1/swift-codes/country/pl")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["countryName"], "POLAND")

        self.branch_data.pop("countryName")
        self.headquarter_data.pop("countryName")

        self.assertEqual(response.data["swiftCodes"][0], self.headquarter_data)
        self.assertEqual(response.data["swiftCodes"][1], self.branch_data)

    def test_iso2_invalid_length(self):
        response = self.client.get("/v1/swift-codes/country/POL")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "ISO2 always has exactly 2 letters.")

    def test_iso2_doesnt_exist(self):
        response = self.client.get("/v1/swift-codes/country/XX")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.data["error"], "Couldn't find country with ISO2 = XX."
        )


# Tests for the third endpoint (POST /v1/swift-codes)
class CreateBankTest(SetUpTest):
    def setUp(self):
        self.create_branch = {
            "address": "789 Test St",
            "bankName": "CREATING BANK",
            "countryISO2": "PL",
            "countryName": "POLAND",
            "isHeadquarter": False,
            "swiftCode": "UVWXYZ12345",
        }

        return super().setUp()

    def test_create_valid_bank_existing_valid_country(self):
        response = self.client.post("/v1/swift-codes", data=self.create_branch)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["message"], "Bank branch created successfully.")

        try:
            _ = BankBranch.objects.get(swift_code=self.create_branch["swiftCode"])
        except BankBranch.DoesNotExist:
            self.fail("Bank branch was not created in the database")

    def test_create_valid_bank_nonexistent_valid_country(self):
        self.create_branch["countryISO2"] = "US"
        self.create_branch["countryName"] = "United States"

        response = self.client.post("/v1/swift-codes", data=self.create_branch)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["message"], "Bank branch created successfully.")

        try:
            country = Country.objects.get(ISO2=self.create_branch["countryISO2"])
            self.assertEqual("UNITED STATES", country.country_name)
        except Country.DoesNotExist:
            self.fail("Failed to create country record in the database")

        try:
            _ = BankBranch.objects.get(swift_code=self.create_branch["swiftCode"])
        except BankBranch.DoesNotExist:
            self.fail("Bank branch was not created in the database")

    def test_create_valid_bank_nonexistent_invalid_country(self):
        self.create_branch["countryISO2"] = "U"
        self.create_branch["countryName"] = "United"

        response = self.client.post("/v1/swift-codes", data=self.create_branch)

        self.assertEqual(response.status_code, 400)

    def test_create_invalid_bank(self):
        data = {
            "wrong": "data",
            "more": "wrong data",
            "false": True,
        }

        response = self.client.post("/v1/swift-codes", data=data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "Incorrect json document.")


# Tests for the fourth endpoint (DELETE /v1/swift-codes)
class DeleteBankEndpointTest(SetUpTest):
    def test_delete_valid_existing_swift_code(self):
        response = self.client.delete("/v1/swift-codes/" + self.branch.swift_code)

        self.assertEqual(response.status_code, 200)

        try:
            _ = BankBranch.objects.get(swift_code=self.branch.swift_code)
            self.fail("Bank branch was not deleted from the database")
        except BankBranch.DoesNotExist:
            pass

    def test_delete_valid_nonexistent_swift_code(self):
        response = self.client.delete("/v1/swift-codes/01234567890")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["error"], "Bank branch not found.")

    def test_delete_invalid_swift_code(self):
        response = self.client.delete("/v1/swift-codes/012345")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "Incorrect length of swift code.")
