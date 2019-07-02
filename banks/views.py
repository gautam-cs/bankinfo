import traceback

from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from banks.authentication import JwtServiceOnlyAuthentication
from banks.models import Branches, Banks
from banks.serializers import BranchSerializer, BankSerializer


# Create your views here.
class LargeResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class BranchView(generics.ListAPIView):
    queryset = Branches.objects.all()
    serializer_class = BranchSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        req_city = self.request.GET.get('city')
        req_ifsc = self.request.GET.get('ifsc')
        req_bank_name = self.request.GET.get('bank_name')
        try:
            if req_ifsc:
                queryset = Branches.objects.filter(ifsc=req_ifsc)

            elif req_city and req_bank_name:
                bank_id = Banks.objects.get(bank_name__contains=req_bank_name).bank_id
                queryset = Branches.objects.filter(city__contains=req_city, bank_id__bank_id=bank_id)
            else:
                queryset = Branches.objects.all()
            return queryset
        except Branches.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def list(self, request, *args, **kwargs):
        self.request = request
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        try:
            serializer = self.get_serializer(queryset, many=True)
            if serializer.is_valid(raise_exception=True):
                return Response(serializer.data)
        except Exception as err:
            traceback.print_tb(err.__traceback__)
            return Response({'message': 'something went wrong', 'status': 'error'})


class BankView(generics.ListAPIView):
    queryset = Banks.objects.all()
    serializer_class = BankSerializer
    pagination_class = LargeResultsSetPagination

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
