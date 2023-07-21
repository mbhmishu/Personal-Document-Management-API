from rest_framework import pagination
from rest_framework.response import Response




class DocumenttSmallesetPagination(pagination.PageNumberPagination):
    page_size=2

    def get_paginated_response(self, data):
        return Response(
            {
                'navigation':{
                    'next_page':self.get_next_link(),
                    'previous_page':self.get_previous_link()
                },
                'page_count':self.page.paginator.count,
                'current_page':self.page.number,
                'results':data
                
            }
        )