from django.views import View
from typing import Optional, Type
from django.db.models import Model
from django.http.response import HttpResponseNotAllowed, HttpResponseNotFound

# models
from typing import Any, Union
from django.shortcuts import HttpResponse
from django.db.models import QuerySet, Model
from django.http import HttpRequest, QueryDict
from django.core.paginator import Paginator


from django.views import View
from django.views.generic.base import ContextMixin

from django.contrib import messages


class ObjectNotFound(Exception):
    pass


class BaseView(ContextMixin, View):
    model: Type[Model] = None
    page_name = None
    default_context = {}
    context_name = "objects"
    paginator = None
    template_name = None

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    def get_context_data(self, data={}, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update({
            "page_name": self.page_name,
            **data
        })

        return context

    def get_message_from_request(self):
        # get messages
        messages_list = [
            (message.tags, message.message)
            for message in messages.get_messages(self.request)
        ]
        return messages_list

    def get_filter_params(self, request: HttpRequest) -> Union[QueryDict, dict]:
        return request.GET.dict()

    def get_queryset(self, *args, **kwargs) -> QuerySet:
        filters: dict = kwargs.get('filters', {})
        if not isinstance(filters, dict):
            filters = {}

        if len(filters.keys()) > 0:
            kwargs.pop("filters")

        queryset = self.model.objects.filter(
            *args, **filters, **kwargs).order_by('-id')

        # if self.paginator is not None:
        #     paginator = Paginator(queryset, self.paginator)
        #     page_number = self.request.GET.get("page")
        #     page_obj = paginator.get_page(page_number)
        #     context = self.get_context_data()
        #     context.update({"page_obj": page_obj})

        return queryset

    def get_object(self, *args, none_when_404=True, **kwargs) -> Optional[Model]:
        filters: dict = kwargs.get('filters', {})
        if not isinstance(filters, dict):
            filters = {}
        
        if len(filters.keys()) > 0:
            kwargs.pop("filters")


        try:
            queryset = self.model.objects.get(*args, **filters, **kwargs,)
            return queryset
        except self.model.DoesNotExist:
            if none_when_404:
                return None
            
            raise ObjectNotFound("Object not found!")

    def with_message(self, context: dict):
        context.update({
            "toasts": self.get_message_from_request()
        })
        return lambda func: func

    def get_previous_page_url(self, default='/'):
        referring_url = self.request.session.get('last_route', default)
        return referring_url

    def get_paginate_object(self, queryset=None, context_name=None):
        if queryset is None:
            queryset = self.get_queryset()
        
        page = self.request.GET.get("page", 1)
        paginator = Paginator(queryset, self.paginator or 25)
        page_obj = paginator.get_page(page)

        return {
            context_name or self.context_name or "objects" : page_obj,
            "paginator": {
                "count": paginator.num_pages,
                "next": page_obj.number + 1 if page_obj.has_next() else None,
                "current": page_obj.number,
                "previous": page_obj.number - 1 if page_obj.has_previous() else None,
                "last_page": paginator.num_pages,
            }
        }

    def on_object_not_found(self):
        return HttpResponseNotFound()

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        try:
            return super().dispatch(request, *args, **kwargs)
        except ObjectNotFound:
            return self.on_object_not_found()


class ActionBaseView(BaseView):
    actions = []

    def __run_action_method(self, action, request, *arg, **kwargs):
        # Check if the method with the provided action name exists
        if hasattr(self, action) and callable(getattr(self, action)):
            # Call the method dynamically
            return getattr(self, action)(request, *arg, **kwargs)
        else:
            return self.on_invalid_action(request, action, *arg, **kwargs)

    def on_invalid_action(self, request, action, *arg, **kwargs):
        return HttpResponseNotAllowed(permitted_methods=['POST'])


    def post(self, request, *args, **kwargs):
        data = request.POST
        action = data.get('action', None)
        if action is None or action not in self.actions:
            return self.on_invalid_action(request, action, *args, **kwargs)
        else:
            return self.__run_action_method(action, request, *args, **kwargs)
