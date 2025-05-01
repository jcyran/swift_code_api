from api.utils.swift_code import *

from .test_setup import SetUpTest


class SwiftCodeTest(SetUpTest):
    def test_normalize_for_headquarters(self):
        swift_code = self.headquarter.swift_code[:8]

        self.assertEqual(swift_code, "ABCDEF12")

        swift_code = normalize_swift_code(swift_code)

        self.assertEqual(swift_code, "ABCDEF12XXX")

    def test_normalize_for_branches(self):
        swift_code = self.branch.swift_code

        swift_code = normalize_swift_code(swift_code)

        self.assertEqual(swift_code, "ABCDEF12345")

    def test_is_headquarter_len11_correct(self):
        swift_code = self.headquarter.swift_code

        self.assertTrue(is_headquarter_swift(swift_code))

    def test_is_headquarter_len8_correct(self):
        swift_code = self.headquarter.swift_code[:8]

        self.assertTrue(is_headquarter_swift(swift_code))

    def test_is_headquarter_incorrect(self):
        swift_code = self.branch.swift_code

        self.assertFalse(is_headquarter_swift(swift_code))

    def test_length_headquarter_len11_valid(self):
        swift_code = self.headquarter.swift_code

        self.assertTrue(is_valid_length_swift(swift_code))

    def test_length_headquarter_len8_valid(self):
        swift_code = self.headquarter.swift_code[:8]

        self.assertTrue(is_valid_length_swift(swift_code))

    def test_length_branch_valid(self):
        swift_code = self.branch.swift_code

        self.assertTrue(is_valid_length_swift(swift_code))

    def test_length_invalid(self):
        swift_code = self.headquarter.swift_code[:7]

        self.assertFalse(is_valid_length_swift(swift_code))

    def test_get_branches_len11_valid(self):
        swift_code = self.headquarter.swift_code

        data = get_bank_branches_swift(swift_code)
        self.branch_data.pop("countryName")

        self.assertEqual(data[0], self.branch_data)

    def test_get_branches_len8_valid(self):
        swift_code = self.headquarter.swift_code[:8]

        data = get_bank_branches_swift(swift_code)
        self.branch_data.pop("countryName")

        self.assertEqual(data[0], self.branch_data)

    def test_get_branches_swift_doesnt_exist(self):
        swift_code = "00000000000"

        data = get_bank_branches_swift(swift_code)

        self.assertEqual(data[0]["error"], "Not a headquarter.")

    def test_get_branches_invalid_len(self):
        swift_code = "00"

        data = get_bank_branches_swift(swift_code)

        self.assertEqual(data[0]["error"], "Invalid swift code length.")
