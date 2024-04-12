from _ast import Expression
from abc import ABC, abstractmethod
from typing import Callable, Tuple, Optional, Union
from enum import Enum


class AstNode(ABC):
    @property
    def childs(self) -> Tuple['AstNode', ...]:
        return ()

    def add_child(self, *ch):
        self.childs += ch

    @abstractmethod
    def __str__(self) -> str:
        pass

    @property
    def tree(self) -> [str, ...]:
        res = [str(self)]
        childs = self.childs
        for i, child in enumerate(childs):
            ch0, ch = '├', '│'
            if i == len(childs) - 1:
                ch0, ch = '└', ' '
            res.extend(((ch0 if j == 0 else ch) + ' ' + s for j, s in enumerate(child.tree)))
        return res

    def visit(self, func: Callable[['AstNode'], None]) -> None:
        func(self)
        map(func, self.childs)

    def __getitem__(self, index):
        return self.childs[index] if index < len(self.childs) else None


class ExprNode(AstNode):
    pass


class ValueNode(ExprNode):
    pass


class NumNode(ValueNode):
    def __init__(self, num: float):
        super().__init__()
        self.num = float(num)

    def __str__(self) -> str:
        return str(self.num)


class IdentNode(ValueNode):
    def __init__(self, name: str):
        super().__init__()
        self.name = str(name)

    def __str__(self) -> str:
        return str(self.name)


class BoolValueNode(ValueNode):
    def __init__(self, name: str):
        super().__init__()
        self.name = str(name)

    def __str__(self) -> str:
        return str(self.name)


class CallNode(ExprNode):
    def __init__(self, func: IdentNode, *params: ExprNode):
        self.func = func
        self.params = params

    @property
    def childs(self) -> Tuple[ExprNode]:
        return self.params

    def __str__(self) -> str:
        return f'call {self.func}'


class BinOp(Enum):
    ADD = '+'
    SUB = '-'
    MUL = '*'
    DIV = '/'
    GE = '>='
    LE = '<='
    NOTEQUALS = '!='
    EQUALS = '=='
    # EQUALS = '='
    GT = '>'
    LT = '<'
    BIT_OR = '||'
    # BIR_AND = '&&'
    BIR_AND = 'and'
    AS = 'as'


class BinOpNode(ValueNode):
    def __init__(self, op: BinOp, arg1: ValueNode, arg2: ValueNode):
        super().__init__()
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2

    @property
    def childs(self) -> Tuple[ValueNode, ValueNode]:
        return self.arg1, self.arg2

    def __str__(self) -> str:
        return str(self.op.value)


class UnOp(Enum):
    NOT = '!'
    SUB = '-'
    AS = 'as'


class UnOpNode(ValueNode):
    def __init__(self, op: UnOp, arg: ValueNode):
        super().__init__()
        self.op = op
        self.arg = arg

    @property
    def childs(self) -> Tuple[ValueNode]:
        return self.arg,

    def __str__(self) -> str:
        return str(self.op.value)


class Join(Enum):
    LEFT = 'left'
    RIGHT = 'right'
    INNER = 'inner'
    FULL = 'full'
    CROSS = 'cross'


class JoinNode(AstNode):
    def __init__(self, join: Join, table1: IdentNode, table2: IdentNode, cond: Optional[ExprNode]):  # ExprNode
        super().__init__()
        self.join = join
        self.table1 = table1
        self.table2 = table2
        self.cond = cond

    @property
    def childs(self):  # -> Tuple[ExprNode]:
        result = [self.table1, self.table2]
        if self.cond:
            result.append(self.cond)
        return tuple(result)
        # return [self.table1, self.table2]  # + [self.cond] if self.cond else ()

    def __str__(self) -> str:
        return f'{self.join} join'


class ExprsNode(AstNode):
    def __init__(self, *exprs: ExprNode):
        super().__init__()
        self.exprs = exprs

    @property
    def childs(self) -> Tuple[ExprNode]:
        return self.exprs

    def __str__(self) -> str:
        return '...'


class GroupByNode(AstNode):
    def __init__(self, *exprs: ExprNode):
        super().__init__()
        self.exprs = exprs

    @property
    def childs(self) -> Tuple[ExprNode]:
        return self.exprs

    def __str__(self) -> str:
        return 'group by'


class OrderByNode(AstNode):
    def __init__(self, *exprs: ExprNode):
        super().__init__()
        self.exprs = exprs

    @property
    def childs(self) -> Tuple[ExprNode]:
        return self.exprs

    def __str__(self) -> str:
        return 'order by'


class SelectNode(AstNode):
    def __init__(self, select_: ExprsNode, from_: Union[IdentNode, JoinNode],
                 where: Optional[ExprNode] = None, group: Optional[GroupByNode] = None,
                 having: Optional[ExprNode] = None, order: Optional[ExprsNode] = None):
        super().__init__()
        self.selects = select_
        self.from_ = from_
        self.where = where
        self.group = group
        self.having = having
        self.order = order

    @property
    def childs(self):  # -> Tuple[AstNode]:
        return [self.selects, self.from_,
                self.where or IdentNode("WITHOUT_WHERE"),
                self.group or IdentNode("WITHOUT_GROUP_BY"),
                self.having or IdentNode("WITHOUT_HAVING"),
                self.order or IdentNode("WITHOUT_ORDER")]

    def __str__(self) -> str:
        return 'select'



