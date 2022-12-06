from sqlalchemy import create_engine, MetaData
import yaml
def load_conf_file(config_file):
   with open(config_file, "r") as f:
       config = yaml.safe_load(f)
       server_conf = config["server"]
       host_conf = server_conf["host"]
       database_conf = server_conf["database"]
       user_conf = server_conf["user"]
       password_conf = server_conf["password"]
   return host_conf, database_conf,user_conf,password_conf
host_conf, database_conf,user_conf,password_conf = load_conf_file("./config/db_config.yml")
engine = create_engine("mysql+pymysql://"+user_conf+":"+password_conf+"@"+host_conf+"/"+database_conf+"")
meta = MetaData()
conn = engine.connect()