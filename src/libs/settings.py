import traceback,sys
import yaml
from .colors import colors

class General:
    def verbose(level:int, value,name="NO_NAME"):
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
            print(colors.ERROR,"[!] Wrong value in verbose()",colors.reset)
    
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
    
    def collect(service:str,function_call) -> dict:
        print(colors.INFO,"[i] AWS.{} : Try collect all information".format(service),colors.reset)
        try:
            data = function_call()
        except Exception:
            print(colors.reset)
            traceback.print_exc()
            print(colors.ERROR,"[!] AWS.{} : An error occurred while collect information".format(service),colors.reset)
            sys.exit(1)
        print(colors.OK,"[+] AWS.{} : All information have been collected".format(service),colors.reset)

        return data

    def create_all_nodes(service:str,function_call,result:dict) -> bool:
        responce = False
        print(colors.INFO,"[i] Neo4j.{} : Try create node and relation".format(service),colors.reset)
        try:
            if function_call(result):
                print(colors.INFO,"[i] Neo4j.{} : You don't have ressource".format(service),colors.reset)
        except Exception:
            print(colors.reset)
            traceback.print_exc()
            print(colors.ERROR,"[!] Neo4j.{} : An error occurred while created node and relation".format(service),colors.reset)
            sys.exit(1)
        print(colors.OK,"[+] Neo4j.{} : All information have been created".format(service),colors.reset)
        return responce

    def association(service:str,associate_service:str,function_call) -> bool:
        response = False
        print(colors.INFO,"[i] Neo4j.Associations : {} and {}".format(service,associate_service),colors.reset)
        try:
            if function_call():
                print(colors.INFO,"[i] Neo4j.Associations : No interconnections for Cloudfront and Route53".format(service,associate_service),colors.reset)
        except Exception:
            print(colors.reset)
            traceback.print_exc()
            print(colors.ERROR,"[!] Neo4j.Associations : An error occurred while created relation".format(service,associate_service),colors.reset)
            sys.exit(1)
        print(colors.OK,"[+] Neo4j.Associations : All relation have been created".format(service,associate_service),colors.reset)
        return response
    
    def get_user_settings(file_name:str) -> list or None:
        try:
            with open(file_name) as setting_file:
                responce = yaml.safe_load(setting_file)
        except FileNotFoundError:
            responce = {}
            print(colors.ERROR,"[!] Error you don't have set your setting file. Default value will be use. Try 'make setup' or 'make reset_setting' to load setting file",colors.reset)
        return responce
    
    def get_user_level_log(user_setting:dict) -> str:
        return user_setting["level_log"] if user_setting.get("level_log") in ["VERBOSE","INFO","ERROR"] else "INFO"

    def get_user_verbose(level_log:str) -> bool:
        return level_log.upper() == "VERBOSE"

    def get_user_pagination(user_setting:dict) -> bool:
        return user_setting["pagination"] if user_setting.get("pagination") else True
    
    def get_user_services(user_setting:dict) -> list:
        services = []
        if user_setting.get("services"):
            for service in user_setting.get("services"):
                services.append(service.lower())
        return services
