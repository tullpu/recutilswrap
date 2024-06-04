from bash import bash

def is_numeric(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def quote_if_necessary(value):
    if is_numeric(value):
        return value
    else:
        return f"'{value}'"


def EQ(field,value):
    return f"{field} = {quote_if_necessary(value)}"

def IN(field,value):
    return f"{field} ~ {quote_if_necessary(value)}"

def OR(*conditions):
    return f"( {' || '.join([c for c in conditions])} )"
def AND(*conditions):
    return f"( {' && '.join([c for c in conditions])} )"

def GT(field,value):
    return f"{field} > {quote_if_necessary(value)}"

def GTE(field,value):
    return f"{field} >= {quote_if_necessary(value)}"

def LT(field,value):
    return f"{field} < {quote_if_necessary(value)}"

def LTE(field,value):
    return f"{field} <= {quote_if_necessary(value)}"


class RecUtilsWrap(object):
    def __init__(self, rec, filename,primarykey):
        self.__rec__ = rec
        self.__filename__ = filename
        self.__pkey__ = primarykey

        self.__prefixargs__ = f" -t {self.__rec__} "
        self.__postfixargs__  = f" {self.__filename__}"


    def create_db(self):
        with open(self.__filename__,'wt') as fp:
            fp.write(f"%rec: {self.__rec__}\n%key: {self.__pkey__}\n%auto: {self.__pkey__}\n")


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
        return EQ(self.__pkey__,value)

    def __expression_by_field__(self,field,value):
        return EQ(field,value)

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



