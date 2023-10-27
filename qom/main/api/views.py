from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView, Response
from django.utils.decorators import method_decorator
from riddlehouse import MonthBooking
from riddlehouse.helpers import functions
from braces.views import CsrfExemptMixin
from game import models as game_models
from orders import models as order_models

class GetMonthCalendar(CsrfExemptMixin, APIView):
    authentication_classes = []

    def post(self, request):
        room_id = request.data.get("room", None)
        month = request.data.get("month", None)
        year = request.data.get("year", None)
        if not room_id or not month:
            return Response("room and month is required", status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        calendar = MonthBooking.Month(month, year).create_calendar(room_id)
        if not calendar:
            return Response({"detail": "Room Not Found"}, status=status.HTTP_404_NOT_FOUND)
        
        print(calendar)
        return Response(data=calendar)


class CheckCoupon(APIView):

    def get(self,request):
        coupon = request.query_params.get("coupon" , None)
        room = request.query_params.get("room" , None)
        if not coupon or not room :
            return Response({"valid" : False , "details" : "کوپن یا اتاق وارد نشده است"} , status=status.HTTP_400_BAD_REQUEST)

        room = get_object_or_404(game_models.Room , pk=room)
        coupon = get_object_or_404(order_models.Coupon , code=coupon)

        is_valid = functions.validate_coupon(room,coupon)

        if not is_valid :
            return Response({"Valid" : False , "Details" : "کد تخفیف وارد شده معتبر نیست"} , status=status.HTTP_403_FORBIDDEN)

        return Response({"valid" : True , "type" : coupon.get_type_display() , "amount" : coupon.amount })


class GetWeekCalendar(CsrfExemptMixin, APIView):
    authentication_classes = []

    def post(self, request):
        calendar = MonthBooking.RoomWeek().create_rooms_list()
        if not calendar:
            return Response({"detail": "Room Not Found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(data=calendar)
