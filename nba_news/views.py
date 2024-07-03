import requests
from bs4 import BeautifulSoup
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.

class NBANewsView(APIView):
    def get(self, request, *args, **kwargs):

        url = "https://tw-nba.udn.com/nba/cate/6754/0/hottest/1"
        response = requests.get(url)

        soup = BeautifulSoup(response.text, 'html.parser')

        div = soup.find('div', class_='pagelink')

        links = soup.find_all('a')
        for link in links:
            print(link.get('href'))

        # h3 = soup.find_all('h3')      # 新聞標題
        # for i in range(7, len(h3)):
        #     print(h3[i].text)

        # b_tag = soup.find_all('b')    # 新聞時間點
        # for i in range(0, len(b_tag)-1):
        #     print(b_tag[i].text)

        # paragraph = soup.find_all('p')    # 新聞內容
        # for i in range(0, len(paragraph)):
        #     print(paragraph[i].text)
    
        return Response({'message': 'success', "payload": []}, status=200)
    

class NBANewsDetailView(APIView):
    def get(self, request, *args, **kwargs):


    
        return Response({'message': 'success', "payload": {}}, status=200)
