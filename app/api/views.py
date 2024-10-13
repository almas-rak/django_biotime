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


class GetMonthlyPunchReport(APIView):
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
            punch_report = zk_api_interaction.get_monthly_punch_report(params=params, user=request.user)
            content = punch_report
        return Response(content)


class EmpSearch(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        params = {
            "employee_icontains": request.query_params.get("employee_icontains"),
            "page_size": 100
        }
        zk_api_interaction = ZkApiInteraction()
        zk_api_interaction.refresh_token()
        if isinstance(zk_api_interaction.token, dict) and 'status_code' in zk_api_interaction.token:
            content = zk_api_interaction.token
        else:
            content = zk_api_interaction.emp_search(params=params, user=request.user)

        return Response(content)





# def emp_search(params_search):
#     session = load_session(username=USER_NAME, password=PASSWORD, code=0)
#     logging.info("Поиск сотрудников из БД")
#     params_s = {
#         "page": 1,
#         "limit": 20,
#         "_p_first_name__contains": params_search,
#     }
#     response_search = session.get(url=f"{BASE_URL_MY}//personnel/employee/table/", params=params_s)
#     response_search = response_search.json()
#     results = response_search["data"]
#     return results
