from parser import *
import os

# todo САМОМУ начать прогонять последовательность. Работает так: входное правило. От него то, что маленькими буквами
#  написано в кавычках - это следующее правило, идём к нему. То, что большими буквами - это токен вроде (то есть к
#  нему идти не надо). Затем создаём узлы для отображения дерева. Узлы супер-простые: просто есть дети и то,
#  что отображает узел. ВСЁ всё работает очень просто. Как уже сказал, нужно просто самому брать и прогонять всё по
#  порядку, начиная со start и select

# todo: может, сначала джойны выводить? А потом столбцы?

s2 = '''
    select age, name, sur
        from table 
        left join t2 on table.first == t2.second
        where age > 7
'''

# left join t2 on g = h
# cross join t2

# s2 = '''
#    SELECT order_id, customer_name
#    FROM orders
#    INNER JOIN customers
#    ON customer_id = customer_id;
# '''

print(*build_tree(s2), sep=os.linesep)
