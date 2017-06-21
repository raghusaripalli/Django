from django.conf.urls import url
from ToDoApp.views import *

urlpatterns = [

    # url(r'^$', mergedview, name='mergedview'),
    # url(r'^home/$',TotalListView.as_view(template_name="index.html"), name="homepage"),
    # url(r'^home/(?P<pk>[0-9]+)/$', ItemsDetailView.as_view(template_name="itemview.html"), name="itemviewpage"),
    # url(r'^create/$', CreateTodoList.as_view(template_name="createlist.html"), name="newlist"),

    # Rest Api's
    url(r'^restlist/$', List_All.as_view(), name="rest_list"),
    url(r'^restlist/(?P<pk>[0-9]+)/$', List_Specific.as_view(), name='rest_list_id'),
    url(r'^restitem/$', Item_All.as_view(), name='rest_item'),
    url(r'^restitem/(?P<pk>[0-9]+)/$', Item_Specific.as_view(), name='rest_item_id'),
    url(r'restlist/(?P<list_id>[0-9]+)/restitem/$', List_Specific_Item.as_view(), name='rest_list_id_item'),
    url(r'restlist/(?P<list_id>[0-9]+)/restitem/(?P<item_id>[0-9]+)/$', List_Specific_Item_Specific.as_view(), name='rest_list_id_item_id')
]