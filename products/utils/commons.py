from django.db.models import Q


class RequestHandler:
    def _request_param(self, request):
        """ 파라미터 값 변수화 """
        data = request.GET.get

        search = data('search', None)
        sort = data('sort', None)

        if sort not in ('created_at', '-created_at', 'total_fund', '-total_fund'):
            # sort가 생성일, 총 펀딩 금액이 아닌 다른 값이 들어왔을 경우 예외 처리
            sort = None

        return search, sort
