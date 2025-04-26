from django.urls import path
from .views import BankBranchCreateUpdateView, BankBranchDetailsView, CountryBankBranchesView

urlpatterns = [
    path('v1/swift-codes', BankBranchCreateUpdateView.as_view(), name='bankbranch-create-delete'),
    path('v1/swift-codes/<str:swift_code>', BankBranchDetailsView.as_view(), name='bankbranch-details'),
    path('v1/swift-codes/country/<str:countryISO2code>', CountryBankBranchesView.as_view(), name='iso2-bankbranches-details'),
]
