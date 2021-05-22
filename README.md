# Обработка кифу  
Для работы программе необходим движок сёги (*.exe). Скачайте любой движок (например, https://github.com/gikou-official/Gikou/releases), поддерживающий USI и разместите его в папке с программой data_processing.py.
Обратите внимание, на корректность выполнения команд движком:
* >usi
* >isready

возвращает readyok
* >usinewgame
* >position startpos moves 7g7f
* >go infinite  
stop

возвращает не только bestmove ..., но и строки вида 

*info depth 1 seldepth 1 time 1 nodes 142 nps 142000 hashfull 0 score cp **-96** multipv 1 pv **3c3d***  

обязательны ненулевые значения для **score cp ...** и **pv ...**
* >go infinite searchmoves 3c3d  
stop

возвращает не только bestmove ..., но и строки вида 

*info depth 2 seldepth 2 time 4 nodes 16145 nps 4036250 hashfull 150 score cp -89 multipv 1 pv **3c3d** 2g2f*  

первое значение **pv ...** обязательно должно соответствовать искомому ходу **searchmoves ...**