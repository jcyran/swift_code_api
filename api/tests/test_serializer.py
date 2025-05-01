from api.serializers import BankBranchSerializer

from .test_setup import SetUpTest


class SerializerTest(SetUpTest):
    # Testing both is_valid() and save() because saving needs to check is_valid() beforehand
    def test_valid_headquarter_valid_data(self):
        serializer = BankBranchSerializer(data=self.headquarter_data)

        self.assertTrue(serializer.is_valid())

        instance = serializer.save()

        self.assertEqual(instance, self.headquarter)

    # Testing both is_valid() and save() because saving needs to check is_valid() beforehand
    def test_valid_branch_valid_data(self):
        serializer = BankBranchSerializer(data=self.branch_data)

        self.assertTrue(serializer.is_valid())

        instance = serializer.save()

        self.assertEqual(instance, self.branch)

    # Testing both is_valid() and save() because saving needs to check is_valid() beforehand
    def test_valid_headquarter_invalid_data(self):
        self.headquarter_data["swiftCode"] = "00000000000"
        serializer = BankBranchSerializer(data=self.headquarter_data)

        self.assertFalse(serializer.is_valid())

    # Testing both is_valid() and save() because saving needs to check is_valid() beforehand
    def test_valid_branch_invalid_data(self):
        self.branch_data["swiftCode"] = "00000000XXX"
        serializer = BankBranchSerializer(data=self.branch_data)

        self.assertTrue(serializer.is_valid())

    def test_invalid_data(self):
        data = {
            "wrong": "data",
            "more": "wrong data",
            "false": True,
        }

        serializer = BankBranchSerializer(data=data)

        self.assertFalse(serializer.is_valid())
