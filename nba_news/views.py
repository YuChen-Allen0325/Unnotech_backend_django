from config import NbaHotNewsConfig
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import NBANews, NBANewsDetail, SideBar
from .serializers import NBANewsSerializer
from .handler.page_parse import SearchLastPage, MutableMainbar, DetailPageInfo, SidebarInfo
# Create your views here.

url = NbaHotNewsConfig.NBA_HOT_NEWS_FIREST_PAGE


class NBANewsView(APIView):
    def get(self, request, *args, **kwargs):

        page_number = int(request.query_params.get(
            'page_number', 1))  # 照著頁碼給參數 沒給就第一頁

        page_size = 10
        offset = (page_number - 1) * page_size

        nba_news = NBANews.objects.all()[offset:offset+page_size].values()

        return Response({'message': 'success', "payload": nba_news}, status=200)


class NBANewsDetailView(APIView):
    def get(self, request, *args, **kwargs):

        nba_news_id = request.query_params.get('nba_news_id')
        return_data = {}

        if nba_news_id == None:
            return Response({'message': 'missing required field', "payload": []}, status=400)

        try:
            nba_news_detail = NBANewsDetail.objects.get(
                nba_news_id=nba_news_id)

            return_data['title'] = nba_news_detail.detail_title
            return_data['author'] = nba_news_detail.author
            return_data['paragraph'] = nba_news_detail.paragraph

            return Response({'message': 'success', "payload": return_data}, status=200)

        except NBANewsDetail.DoesNotExist:
            return Response({'message': 'Data not found', "payload": []}, status=400)


class SideBarView(APIView):
    def get(self, request, *args, **kwargs):

        sidebar_info = SidebarInfo(url)

        return Response({'message': 'success', "payload": sidebar_info}, status=200)


class CronJobView(APIView):
    def get(self, request, *args, **kwargs):

        first_slash_from_bottom = url.rfind('/')
        url_without_page = url[:first_slash_from_bottom + 1]

        last_page = SearchLastPage(url)

        insert_data = []
        filter_data = []
        detail_page_data = []

        for i in range(1, (last_page+1)):   # 爬資料
            mutable_url = url_without_page + str(i)
            a, b = MutableMainbar(mutable_url)

            insert_data += a
            filter_data += b

        nba_news = NBANews.objects.filter(detail_url__in=filter_data)
        detail_url_amount = len(filter_data)

        if detail_url_amount == len(nba_news):
            return Response({'message': 'Nothing to update', "payload": []}, status=200)

        nba_all_obj = NBANews.objects.all()
        nba_all_detail_obj = NBANewsDetail.objects.all()
        nba_all_obj.delete()
        nba_all_detail_obj.delete()

        serializer = NBANewsSerializer(data=insert_data, many=True)

        for detail_url in filter_data:
            data = DetailPageInfo(detail_url)
            detail_page_data += data

        if serializer.is_valid():
            instances = [NBANews(**item) for item in serializer.validated_data]
            insert_infos = NBANews.objects.bulk_create(instances)
            for i in range(len(insert_infos)):
                detail_page_data[i]["nba_news_id"] = insert_infos[i].id
                NBANewsDetail.objects.create(**detail_page_data[i])

        # Websocket

        return Response({'message': 'success', "payload": []}, status=200)
