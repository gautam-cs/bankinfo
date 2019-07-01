from django.conf.urls import url

from banks.views import BranchView, BankView

urlpatterns = [
    url(r'^branch', BranchView.as_view(), name='branches'),
    url(r'^bank', BankView.as_view(), name='banks')
]
