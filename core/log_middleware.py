import logging

logger = logging.getLogger('django')

class LogRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 요청 파라미터 로깅
        if request.method == 'GET':
            parameters = request.GET.dict()
        elif request.method in ['POST', 'PUT']:
            parameters = request.POST.dict()
        else:
            parameters = {}

        # 요청 헤더 로깅
        headers = dict(request.headers)
        # 'Cookie'와 같이 민감한 정보를 포함할 수 있는 헤더는 제외할 수 있습니다.
        headers.pop('Cookie', None)

        # 요청 정보 로깅
        logger.info(f"Request path: {request.path}")
        logger.info(f"Request method: {request.method}")
        logger.info(f"Request parameters: {parameters}")
        logger.info(f"Request headers: {headers}")

        response = self.get_response(request)

        # 응답 정보 로깅
        logger.info(f"Response status code: {response.status_code}")
        # 응답 내용은 크기가 크거나 이진 데이터일 수 있으므로 로깅에서 제외할 수 있습니다.
        logger.info(f"Response content: {response.content}")

        return response
