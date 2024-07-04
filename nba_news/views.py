from config import NbaHotNewsConfig
from rest_framework.views import APIView
from rest_framework.response import Response
from .handler.page_parse import SearchLastPage, MutableMainbar, DetailPageInfo, SidebarInfo
# Create your views here.

url = NbaHotNewsConfig.NBA_HOT_NEWS_FIREST_PAGE

class NBANewsView(APIView):
    def get(self, request, *args, **kwargs):



        return Response({'message': 'success', "payload": {}}, status=200)


class NBANewsDetailView(APIView):
    def get(self, request, *args, **kwargs):

        return Response({'message': 'success', "payload": {}}, status=200)

class SideBarView(APIView):
    def get(self, request, *args, **kwargs):

        sidebar_info = SidebarInfo(url)

        return Response({'message': 'success', "payload": sidebar_info}, status=200)
    

class CronJobView(APIView):
    def get(self, request, *args, **kwargs):
        
        first_slash_from_bottom = url.rfind('/')
        url_without_page = url[:first_slash_from_bottom + 1]

        last_page = SearchLastPage(url)

        for i in range(1, (last_page+1)):   # 搜尋+判斷
            mutable_url = url_without_page + str(i)
            a, b = MutableMainbar(mutable_url)


        return Response({'message': 'success', "payload": {"last_page": last_page, "stored_data": a, "filter": b}}, status=200)
    
