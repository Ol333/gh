import subprocess
import yadisk
from datetim import datetime

if __name__ == "__main__":
    y = yadisk.YaDisk(token="AQAAAAAahgXXAAciB3tbnuoQtkG1muQjqowmVeA")
    print(y.check_token())
    for i in range(100): #запускаем первых 100 человек (а всего 2622)
        print(i)
        subprocess.run(["python","data_processing.py",str(i)], shell=False)
        #https://ramziv.com/blog-detail/2
        date_time = datetime.strftime(datetime.now(),"%d.%m.%Y-%H.%M.%S")
        y.mkdir('/bakup/{}'.format(date_time))
        #y.upload("shogi_db.db", "/backup/{}/shogi_db.db".format(date_time))
        y.upload("test.txt", "/backup/{}/test.txt".format(date_time))
        
