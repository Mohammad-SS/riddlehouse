from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.views import APIView, Response
from django.utils.decorators import method_decorator
from riddlehouse import MonthBooking
from braces.views import CsrfExemptMixin


class GetMonthCalendar(CsrfExemptMixin, APIView):
    authentication_classes = []

    def post(self, request):
        room_id = request.data.get("room", None)
        month = request.data.get("month", None)
        year = request.data.get("year", None)
        if not room_id or not month:
            return Response("room and month is required", status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        calendar = MonthBooking.Month(month, year).create_calander(room_id)
        if not calendar:
            return Response({"detail": "Room Not Found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(data=calendar)
