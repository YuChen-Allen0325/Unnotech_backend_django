import copy
import requests
from config import NbaHotNewsConfig
from rest_framework.views import APIView
from rest_framework.response import Response
from .handler.page_parse import SearchLastPage, MutableMainbar, DetailPageInfo
# Create your views here.


class NBANewsView(APIView):
    def get(self, request, *args, **kwargs):

        url = NbaHotNewsConfig.NBA_HOT_NEWS_FIREST_PAGE

        last_page = SearchLastPage(url)
        a, b = MutableMainbar(url)

        return Response({'message': 'success', "payload": {"last_page": last_page, "stored_data": a, "filter": b}}, status=200)


class NBANewsDetailView(APIView):
    def get(self, request, *args, **kwargs):

        return Response({'message': 'success', "payload": {}}, status=200)
