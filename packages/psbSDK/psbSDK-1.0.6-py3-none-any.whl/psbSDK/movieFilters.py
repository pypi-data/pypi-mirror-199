from collections import defaultdict

class Filters:
    def __init__(self):
        self.filters = defaultdict(list)
        self.FILTERING_OPERATORS = {
            "eq": "=",
            "neq": "!=",
            "not": "!",
            "gte": ">=",
            "lte": "<=",
            "gt": ">",
            "lt": "<"
        }
    
    def add_filter(self, oper=None, field=None, value=None):
        if oper in self.FILTERING_OPERATORS.keys() and (field and oper and value):
            self.filters[self.FILTERING_OPERATORS[oper]].append([field, value])
        else:
            raise Exception("Invalid Filters")
        
    def is_exist(self, field=None, isExist=True):
        if field == "id":
            field = "_id"
        if isExist:
            self.filters[""].append([None, field])
        else:
            self.filters[self.FILTERING_OPERATORS["not"]].append([None, field])
    
    def sort(self, field=None, isAsc=True):
        if field == "id":
            field = "_id"
        srt = "asc"
        if not isAsc:
            srt = "desc"
        self.filters[self.FILTERING_OPERATORS["eq"]].append(["sort", str(field)+":"+srt])

    def set_offset(self, offset):
        if offset:
            self.filters[self.FILTERING_OPERATORS["eq"]].append(["offset", str(offset)])
    
    def set_limit(self, limit):
        if limit:
            self.filters[self.FILTERING_OPERATORS["eq"]].append(["limit", str(limit)])

    def set_page(self, page):
        if page:
            self.filters[self.FILTERING_OPERATORS["eq"]].append(["page", str(page)])


