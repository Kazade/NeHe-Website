from django.core.paginator import Paginator as DPaginator
from django.core.paginator import Page

class Paginator(DPaginator):
    def page(self, number):
        "Returns a Page object for the given 1-based page number."
        number = self.validate_number(number)
        offset = (number - 1) * self.per_page
        if offset + self.per_page + self.orphans >= self.count:
            offset = self.count
        return Page(self.object_list.fetch(self.per_page, offset), number, self)
