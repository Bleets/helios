import traceback,sys

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
    
    async def collect(service:str,function_call) -> dict:
        print(colors.INFO,"[i] AWS.{} : Try collect all information".format(service),colors.reset)
        try:
            data = await function_call()
        except Exception:
            print(colors.reset)
            traceback.print_exc()
            print(colors.ERROR,"[!] AWS.{} : An error occurred while collect information".format(service),colors.reset)
            sys.exit(1)
        print(colors.OK,"[+] AWS.{} : All information have been collected".format(service),colors.reset)

        return data