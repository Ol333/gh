import subprocess
import yadisk
from datetime import datetime

#https://ramziv.com/blog-detail/2
#https://oauth.yandex.ru/
#https://oauth.yandex.ru/authorize?response_type=token&client_id=ID _ПРИЛОЖЕНИЯ

if __name__ == "__main__":
    y = yadisk.YaDisk(token="AQAAAAAahgXXAAciB3tbnuoQtkG1muQjqowmVeA")
    print(y.check_token())
    for i in range(100): #запускаем первых 100 человек (а всего 2622)
        print(i)
        subprocess.run(["python","data_processing.py",str(i)], shell=False
        date_time = datetime.strftime(datetime.now(),"%d.%m.%Y-%H.%M.%S")
        y.mkdir('/backup/{}'.format(date_time))
        y.upload("shogi_db.db", "/backup/{}/shogi_db.db".format(date_time))
