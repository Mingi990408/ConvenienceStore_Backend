
import pymysql

# SQL 적용
host ='event.cdjb7q86vnre.ap-northeast-2.rds.amazonaws.com'
port = 3306
database = 'event'
username = 'admin'
password ='19991003'

conn = pymysql.connect(host = host, 
                       user = username, 
                       passwd = password, 
                       db = database, 
                       port = port, 
                       charset = 'utf8')