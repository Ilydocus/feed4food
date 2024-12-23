from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import get_post_report, get_item_attributes
from .views import ItemAutocomplete


urlpatterns = [
    path('report_form', login_required(get_post_report), name='report_form'),
    path('get_item/<str:name>', login_required(get_item_attributes), name='get_item_attributes'),
    path('item-autocomplete/', ItemAutocomplete.as_view(), name='item-autocomplete'),

    # path('preview', login_required(preview_form), name='preview_form'),
]
