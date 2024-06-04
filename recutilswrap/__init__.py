from bash import bash


def quote_if_necessary(value):
    if ' ' in str(value):
        return f"\"{value}\""
    else:
        return value


def check_equals(field,value):
    return f"{field} = {quote_if_necessary(value)}"

def check_contains(field,value):
    return f"{field} ~ {quote_if_necessary(value)}"

def check_or(*conditions):
    return f"( {' || '.join([c for c in conditions])} )"
def check_and(*conditions):
    return f"( {' && '.join([c for c in conditions])} )"

def check_gt(field,value):
    return f"{field} > {quote_if_necessary(value)}"

def check_gte(field,value):
    return f"{field} >= {quote_if_necessary(value)}"

def check_lt(field,value):
    return f"{field} < {quote_if_necessary(value)}"

def check_lte(field,value):
    return f"{field} <= {quote_if_necessary(value)}"


class RecUtilsWrap(object):
    def __init__(self, rec, filename,primarykey):
        self.__rec__ = rec
        self.__filename__ = filename
        self.__pkey__ = primarykey

        self.__prefixargs__ = f" -t {self.__rec__} "
        self.__postfixargs__  = f" {self.__filename__}"

    def parse(self,output:str):

        def parse_block(block:str):
            output = {}
            lines = block.split("\n")
            for line in lines:
                key,value = line.split(': ')
                if key == 'tags':
                    value = value.split(' ')
                output[key] = value
            return output

        blocks = output.split("\n\n")
        return [parse_block(block) for block in blocks]


    def __expression_by_key__(self,value):
        return check_equals(self.__pkey__,value)


    def bash(self,cmd,argstr=''):
        return str(bash(f"{cmd} {self.__prefixargs__} {argstr} {self.__postfixargs__}"))


    def select(self,expression):
        return self.parse(self.bash('recsel', f"-e \"{expression}\""))

    def all(self):
        return self.parse(self.bash('recsel'))

    def insert(self,**kwargs):
        expression = ' '.join([ f"-f {k} -v \"{v}\"" for k,v in kwargs.items()])
        return self.bash('recins',expression)

    def delete(self,kvalue):
        expression = self.__expression_by_key__(kvalue);
        return self.bash('recdel', f"-e \"{expression}\"")

    def update(self,kvalue,**kwargs):
        condition = self.__expression_by_key__(self,kvalue);
        expression = ' '.join([ f"-t {k} -v \"{v}\"" for k,v in kwargs.items()])
        return self.bash('recset', f"-e \"{condition}\" {expression}")



