from py2neo import Graph

from .colors import colors

class General:
    def verbose(level:int,value,name="NO_NAME"):
        if type(name) == str and level and value:
            if level >= 3:
                print(colors.VERBOSE,'[v] {}.type = "{}"| {} = "{}" '.format(
                            name,
                            type(name),
                            name, 
                            value
                    ),colors.reset)
            else:
                if name == "NO_NAME":
                    print(colors.VERBOSE,'[v] "{}" '.format(value),colors.reset)
                else:
                    print(colors.VERBOSE,'[v] {} = "{}" '.format(name,value),colors.reset)
        else:
            print(colors.ERROR,"[!] Wrong value in verbose()")
    
    def filter_data(data:dict,elements:list):
        filtered_data = {}

        for element in elements:
            if type(element) == str:
                filtered_data.update({element:data[element]})
            else:
                if len(element) == 2:
                    if element[1] == "Items":
                        filtered_data.update({element[0]:data[element[0]][element[1]]})
                    else:
                        filtered_data.update({element[1]:data[element[0]][element[1]]})

        return filtered_data