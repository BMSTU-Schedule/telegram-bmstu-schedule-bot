import re

GROUP_CODE_REGEX = r'^[а-яА-Я]{1,4}\d{0,2}\-\d{1,3}[а-яА-Я]?$'
GC_REG_MATCHER = re.compile(GROUP_CODE_REGEX)

class Group:
    def __init__(self, name="", group_type=""):
        self.name = name
        self.group_type = group_type
    
    def __str__(self):
        return self.name + self.group_type

    def has_type(self):
        return len(self.group_type) != 0
    
    def get(self):
        return self.name + self.group_type

def parse_group(text):
    if GC_REG_MATCHER.match(text):
        text = text.upper()
        group = Group()
        if text[len(text)-1].isalpha():
            group.name = text[:len(text)-1]
            group.group_type = text[len(text)-1:]
        else:
            group.name = text
        return group
    return None