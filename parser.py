import ply.lex as lex
from ast_nodes import *
import ply.yacc as yacc

tokens = [
    'NUMBER', 'IDENT',
    'ADD', 'SUB', 'MUL', 'DIV', 'MOD',
    # 'ASSIGN',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'SEMICOLON',
    'GT', 'LT', 'GE', 'LE',
    'EQUALS', 'NOTEQUALS',
    'GT_INPUT', 'LT_OUTPUT',
    'OR', 'NOT',
    'COMMA', 'DOT'
]

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'while': 'WHILE',
    'do': 'DO',
    'int': 'TINT',
    'bool': 'BOOL',
    'char': 'CHAR',
    'true': 'TRUE',
    'false': 'FALSE',
    'inner': 'INNER',
    'outer': 'OUTER',
    'left': 'LEFT',
    'right': 'RIGHT',
    'full': 'FULL',
    'cross': 'CROSS',
    'join': 'JOIN',
    'on': 'ON',
    'where': 'WHERE',
    'group': 'GROUP',
    'having': 'HAVING',
    'by': 'BY',
    'order': 'ORDER',
    'select': 'SELECT',
    'from': 'FROM',
    'and': 'AND',
    'as': 'AS'
}

tokens += reserved.values()

t_ADD = r'\+'
t_SUB = r'-'
t_MUL = r'\*'
t_DIV = r'/'
t_MOD = r'%'
# t_ASSIGN = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'{'
t_RBRACE = r'}'
t_SEMICOLON = r';'
t_GT = r'>'
t_LT = r'<'
t_EQUALS = r'=='
# t_EQUALS = r'='
t_NOTEQUALS = r'!='
t_GE = r'>='
t_LE = r'<='
t_OR = r'\|\|'
# t_AND = r'&&'
t_NOT = r'!'
t_GT_INPUT = r'>>'
t_LT_OUTPUT = r'<<'
t_COMMA = r','
t_DOT = r'.'

t_ignore = ' \r\t'


# абстрактный идентификатор (просто комбинация символов, которую нужно парсить)
def t_IDENT(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*\.?[a-zA-Z0-9_]*'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t


def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t


def t_ccode_comment(t):
    r'(/\*(.|\n)*?\*/)|(//.*)'
    pass


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()


########################################################################

def p_start(t):
    ''' start : select '''
    t[0] = t[1]


def p_number(t):
    ''' number : NUMBER '''
    t[0] = NumNode(t[1])


def p_ident(t):
    ''' ident : IDENT '''
    t[0] = IdentNode(t[1])


def p_params(t):
    ''' params :
            | expr
            | params COMMA expr
    '''
    if len(t) == 1:
        t[0] = []
    else:
        t[0] = [*t[1], t[3]] if len(t) > 2 else [t[1]]


def p_call(t):
    ''' call : ident LPAREN params RPAREN '''
    t[0] = CallNode(t[1], *t[3])


def p_group(t):
    ''' group : ident
              | number
              | LPAREN expr RPAREN
              | call
    '''
    t[0] = t[2] if len(t) > 2 else t[1]


def p_not(t):
    ''' not : group
            | NOT group
    '''
    t[0] = UnOpNode(UnOp(t[1]), t[2]) if len(t) > 2 else t[1]


def p_mult(t):
    ''' mult : not
             | mult MUL not
             | mult DIV not
             | mult MOD not
    '''
    t[0] = BinOpNode(BinOp(t[2]), t[1], t[3]) if len(t) > 2 else t[1]


def p_add(t):
    ''' add : mult
             | add ADD mult
             | add SUB mult
    '''
    t[0] = BinOpNode(BinOp(t[2]), t[1], t[3]) if len(t) > 2 else t[1]


def p_compare(t):
    ''' compare : add
            | add GE add
            | add LE add
            | add GT add
            | add LT add
            | add EQUALS add
            | add NOTEQUALS add
    '''
    t[0] = BinOpNode(BinOp(t[2]), t[1], t[3]) if len(t) > 2 else t[1]


def p_and(t):
    ''' and : compare
            | and AND compare
    '''
    t[0] = BinOpNode(BinOp(t[2]), t[1], t[3]) if len(t) > 2 else t[1]


# 6
def p_or(t):
    ''' or : and
            | or OR and
    '''
    t[0] = BinOpNode(BinOp(t[2]), t[1], t[3]) if len(t) > 2 else t[1]


def p_expr(t):  # todo редактирую
    ''' expr : or
    '''
    t[0] = t[1]
    # if len(t) == 2:
    #     t[0] = t[1]
    # elif len(t) == 3:
    #     t[0] = UnOpNode(UnOp(t[1]), t[2])


def p_join(t):
    ''' join : ident
            | join LEFT JOIN ident ON expr
            | join RIGHT JOIN ident ON expr
            | join FULL JOIN ident ON expr
            | join INNER JOIN ident ON expr
            | join CROSS JOIN ident
    '''
    if len(t) == 2:
        t[0] = t[1]  # и тогда вернётся IdentNode
    else:
        cond = t[6] if len(t) > 6 else None
        t[0] = JoinNode(Join(t[2]), t[1], t[4], cond)  # а тут JoinNode


def p_column_name(t):
    ''' column_name : ident
                | column_name AS ident
    '''
    if len(t) == 2:
        t[0] = t[1]
    elif len(t) == 4:
        # t[0] = UnOpNode(UnOp(t[2]), t[3])
        t[0] = BinOpNode(BinOp(t[2]), t[1], t[3])


def p_separated_exprs(t):  # с помощью этого разбирается множество параметров
    ''' separated_exprs : column_name
            | separated_exprs COMMA separated_exprs '''
    t[0] = [*t[1], *t[3]] if len(t) > 2 else [t[1]]


def p_exprs(t):
    ''' exprs : separated_exprs '''
    t[0] = ExprsNode(*t[1])


def p_exprs_for_group_by(t):
    ''' exprs_for_group_by : separated_exprs '''
    t[0] = GroupByNode(*t[1])


def p_exprs_for_order_by(t):  # todo: не придумал, как сделать, чтобы можно было оставлять пустым
    ''' exprs_for_order_by : separated_exprs '''
    t[0] = OrderByNode(*t[1])
    # if len(t) == 1:
    #     t[0] = None
    # elif len(t) == 2:
    #     t[0] = OrderByNode(*t[1])


def p_select(t):  # todo: ещё функции max, count, avg, sum ; доработать having
    ''' select : SELECT exprs FROM join
                | SELECT exprs FROM join WHERE expr
                | SELECT exprs FROM join WHERE expr GROUP BY exprs_for_group_by
                | SELECT exprs FROM join GROUP BY exprs_for_group_by

                | SELECT exprs FROM join WHERE expr GROUP BY exprs_for_group_by HAVING expr
                | SELECT exprs FROM join WHERE expr GROUP BY exprs_for_group_by HAVING expr ORDER BY exprs_for_order_by

                | SELECT exprs FROM join GROUP BY exprs_for_group_by HAVING expr
                | SELECT exprs FROM join GROUP BY exprs_for_group_by HAVING expr ORDER BY exprs_for_order_by
    '''

    select_node = None
    from_node = None
    where_node = None
    group_node = None
    having_node = None
    order_node = None

    for i in range(len(t)):
        if t[i] == 'select':
            select_node = t[i+1]
        elif t[i] == 'from':
            from_node = t[i+1]
        elif t[i] == 'where':
            where_node = t[i+1]
        elif t[i] == 'group':
            group_node = t[i + 2]
        elif t[i] == 'having':
            having_node = t[i + 1]  # todo
        elif t[i] == 'order':
            order_node = t[i + 2]  # todo

    t[0] = SelectNode(select_node, from_node, where_node, group_node, having_node, order_node)

    # if len(t) == 5:
    #     t[0] = SelectNode(t[2], t[4])
    # elif t[5] == 'where':
    #     if len(t) > 7 and t[7] == 'group':
    #         exprs_node = t[2]
    #         join_node = t[4]
    #         where_node = t[6]
    #         group_node = t[9]
    #         t[0] = SelectNode(exprs_node, join_node, where_node, group_node)
    #     else:
    #         t[0] = SelectNode(t[2], t[4], t[6])
    # elif t[5] == 'group':
    #     t[0] = SelectNode(t[2], t[4], None, t[7])


def p_error(t):
    print("Syntax error in input!")


parser = yacc.yacc()


def build_tree(s):
    result = parser.parse(s)
    return result.tree
