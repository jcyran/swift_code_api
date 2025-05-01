from django.db import models


class Country(models.Model):
    ISO2 = models.CharField(
        max_length=2, primary_key=True
    )  # ISO2 always uses 2 digit codes
    country_name = models.CharField(max_length=255)

    def __str__(self):
        return self.country_name


class BankBranch(models.Model):
    swift_code = models.CharField(
        max_length=11, primary_key=True
    )  # SWIFT codes are 8 digits for headquarters + 3 for bank branches
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=255)
    bank_address = models.CharField(max_length=255)

    def __str__(self):
        return self.bank_name
