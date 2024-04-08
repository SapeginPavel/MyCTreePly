from parser import *
import os

s = '''
        bool a = true;
        int b ;
        /* comment 1
        cin >> c
        */

        cin >> a;
        b = a + a * 10;;

        for (int i = 0; i < 5; i = i + 2)
            cout << b;

        while (true){
            if (a > b + 1 & x) {
                cout << b;  // comment 2
                a = 0;
            }
            else
                if (8 > 9)
                    cout << a;
                else {
                    a=9;}

            a = 90;
        }

        do{
            cout << a - b;
            a = a - b;
        } while (!a != (1 + 9) * b / 8);

    '''

s1 = '''int a = -(2 + 1);
        cin >> a;

        {
            if (a==5)
                { }
            int l = 90;
        }

        int l =97;
        ;;;;
         '''

# todo САМОМУ начать прогонять последовательность. Работает так: входное правило. От него то, что маленькими буквами написано в кавычках - это следующее правило, идём к нему. То, что большими буквами - это токен вроде (то есть к нему идти не надо). Затем создаём узлы для отображения дерева. Узлы супер-простые: просто есть дети и то, что отображает узел. ВСЁ
# всё работает очень просто. Как уже сказал, нужно просто самому брать и прогонять всё по порядку, начиная со start и select

s2 = '''
    select age, name, sur
        from table 
        left join t2 on t = 78
        where age > 7
'''

# s2 = '''
#    SELECT order_id, customer_name
#    FROM orders
#    INNER JOIN customers
#    ON customer_id = customer_id;
# '''

print(*build_tree(s2), sep=os.linesep)

# TODO Нужно понять, почему не работает следующий код:
# s2 = '''
#     select 5, a, 3+a*(6-5+b) > 6 && 7>9 || a(3, a+4)
#         from table /* left join t2 on t = 78  todo*/
#         where a > 7
# '''
