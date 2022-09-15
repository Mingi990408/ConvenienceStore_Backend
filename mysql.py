from pandas import DataFrame
import pymysql

class Product:
    def __init__(self, event = None, name = None, price = None, img = None, df: DataFrame = None) -> None:
        self.brand = 'GS25'
        self.event = event
        self.name = name
        self.price = price
        self.img = img 
        self.df = df

    def save(self):
        host ='event.cdjb7q86vnre.ap-northeast-2.rds.amazonaws.com'
        port = 58321
        database = 'sys'
        username = 'admin'
        password ='19991003'

        conn = pymysql.connect(
            host = host, 
            user = username, 
            passwd = password, 
            db = database, 
            port = port, 
            charset = 'utf8')

        cursors = conn.cursor()
        
        if self.df is None:
            value = (self.brand, self.event, self.name, self.price, self.img)
            cursors.execute('INSERT IGNORE INTO cvs (brand, event, name, price, img) VALUES (%s, %s, %s, %s, %s)', value)
        
        else:
            for _, row in self.df.iterrows():                              # DataFrame의 각 행을 하나씩 가져옴 
                value = (row[0], row[1], row[2], row[3], row[4])        # brand, event, name, price, img 순 
                cursors.execute("INSERT IGNORE INTO cvs (brand, event, name, price, img) VALUES (%s, %s, %s, %s, %s)", value)   # mysql에 DataFrame 저장 

        conn.commit()
        conn.close()