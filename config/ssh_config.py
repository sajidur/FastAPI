from sqlalchemy import create_engine, MetaData
import yaml
def load_conf_file(config_file="./config/ssh_config.yml"):
   with open(config_file, "r") as f:
       config = yaml.safe_load(f)
       server_conf = config["server"]
       host_conf = server_conf["host"]
       user_conf = server_conf["user"]
       password_conf = server_conf["password"]
   return host_conf, user_conf,password_conf

host_conf,user_conf,password_conf =load_conf_file()