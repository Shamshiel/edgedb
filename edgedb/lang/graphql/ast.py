##
# Copyright (c) 2016 MagicStack Inc.
# All rights reserved.
#
# See LICENSE for details.
##


import re

from edgedb.lang.common import ast, parsing


class Base(ast.AST):
    ns = 'graphql'

    __ast_hidden__ = {'context'}
    context: parsing.ParserContext = None

    def _extra_repr(self):
        return ''

    def __repr__(self):
        ar = self._extra_repr()
        return '<{}.{} at {:#x}{}>'.format(self.__class__.ns,
                                           self.__class__.__name__,
                                           id(self),
                                           ar)


class LiteralNode(Base):
    value: object

    def topython(self):
        return self.value


class StringLiteral(LiteralNode):
    def tosource(self):
        value = self.value
        # generic substitutions for '\b' and '\f'
        #
        value = value.replace('\b', '\\b').replace('\f', '\\f')
        value = repr(value)
        # escape \b \f \u1234 and \/ correctly
        #
        value = re.sub(r'\\\\([fb])', r'\\\1', value)
        value = re.sub(r'\\\\(u[0-9a-fA-F]{4})', r'\\\1', value)
        value = value.replace('/', r'\/')

        if value[0] == "'":
            # need to change quotation style
            #
            value = value[1:-1].replace(R'\'', "'").replace('"', R'\"')
            value = '"' + value + '"'

        return value


class IntegerLiteral(LiteralNode):
    pass


class FloatLiteral(LiteralNode):
    pass


class BooleanLiteral(LiteralNode):
    pass


class EnumLiteral(LiteralNode):
    pass


class ListLiteral(LiteralNode):
    def topython(self):
        return [val.topython() for val in self.value]


class ObjectLiteral(LiteralNode):
    def topython(self):
        return {field.name: field.value.topython() for field in self.value}


class Variable(Base):
    value: object


class Document(Base):
    definitions: list


class Definition(Base):
    name: str = None
    selection_set: object


class OperationDefinition(Definition):
    type: str = None
    variables: list
    directives: list


class FragmentDefinition(Definition):
    on: object
    directives: list


class VariableDefinition(Base):
    name: object
    type: object
    value: object


class VariableType(Base):
    name: object
    nullable: bool = True
    list: bool = False


class SelectionSet(Base):
    selections: list


class Selection(Base):
    pass


class Field(Selection):
    alias: str = None
    name: object = None
    arguments: list
    directives: list
    selection_set: object


class FragmentSpread(Selection):
    name: object
    directives: list


class InlineFragment(Selection):
    on: object
    directives: list
    selection_set: object


class Directive(Base):
    name: object
    arguments: list


class Argument(Base):
    name: object
    value: object


class ObjectField(Base):
    name: object
    value: object
