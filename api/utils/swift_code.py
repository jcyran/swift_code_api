from api.models import BankBranch


def normalize_swift_code(code: str) -> str:
    return code if len(code) == 11 else code + "XXX"


def is_headquarter_swift(code: str) -> bool:
    return code.endswith("XXX") or len(code) == 8


def is_valid_length_swift(code: str) -> bool:
    return len(code) in (8, 11)


def get_bank_branches_swift(code: str) -> list:
    if not is_valid_length_swift(code):
        return [{"error": "Invalid swift code length."}]
    elif not is_headquarter_swift(code):
        return [{"error": "Not a headquarter."}]

    data = []

    branches = BankBranch.objects.filter(swift_code__startswith=code[:8])

    for branch in branches:
        if is_headquarter_swift(branch.swift_code):
            continue

        data.append(
            {
                "address": branch.bank_address,
                "bankName": branch.bank_name,
                "countryISO2": branch.country.ISO2,
                "isHeadquarter": False,
                "swiftCode": branch.swift_code,
            }
        )

    return data
