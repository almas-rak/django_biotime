from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from zk_services.views import ZkApiInteraction


class GetEmp(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        zk_api_interaction = ZkApiInteraction()
        zk_api_interaction.refresh_token()
        if isinstance(zk_api_interaction.token, dict) and 'status_code' in zk_api_interaction.token:
            content = zk_api_interaction.token
        else:
            emp = zk_api_interaction.get_emp(user=request.user)
            content = {'data': emp}
        return Response(content)


class GetMonthlyStatusReport(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        employees = request.query_params.get("employees")
        if not start_date:
            return Response({"error": f"Нет параметра: start_date"}, status=status.HTTP_400_BAD_REQUEST)
        if not end_date:
            return Response({"error": f"Нет параметра: end_date"}, status=status.HTTP_400_BAD_REQUEST)
        if not employees:
            return Response({"error": f"Нет параметра: employees"}, status=status.HTTP_400_BAD_REQUEST)
        zk_api_interaction = ZkApiInteraction()
        zk_api_interaction.refresh_token()
        if isinstance(zk_api_interaction.token, dict) and 'status_code' in zk_api_interaction.token:
            content = zk_api_interaction.token
        else:
            params = {
                "start_date": start_date,
                "end_date": end_date,
                "employees": employees,
                "page_size": 100
            }
            status_report = zk_api_interaction.get_monthly_status_report(params=params, user=request.user)
            content = status_report
        return Response(content)
