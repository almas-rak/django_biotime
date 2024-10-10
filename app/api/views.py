from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from zk_services.views import ZkApiInteraction


class GetEmp(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        zk_api_interaction = ZkApiInteraction()
        if isinstance(zk_api_interaction.token, dict) and 'status_code' in zk_api_interaction.token:
            content = zk_api_interaction.token
        else:
            emp = zk_api_interaction.get_emp(user_pk=request.user)
            content = {'data': emp}
        return Response(content)
