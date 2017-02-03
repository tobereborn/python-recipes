#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by weizhenjin on 17-2-3

"""
A recursive descent parser example.
Usage:
    python rparser.py [options] <inputfile>
Options:
    ­h, ­­help      Display this help message.
Example:
    python rparser.py myfile.txt
The grammar:
    Prog ::= Command | Command Prog
    Command ::= Func_call
    Func_call ::= Term '(' Func_call_list ')'
    Func_call_list ::= Func_call | Func_call ',' Func_call_list
    Term = <word>
"""

import sys
import string
import types
import getopt

#
# To use the IPython interactive shell to inspect your running
#   application, uncomment the following lines:
#
# from IPython.Shell import IPShellEmbed
# ipshell = IPShellEmbed((),
#     banner = '>>>>>>>> Into IPython >>>>>>>>',
#     exit_msg = '<<<<<<<< Out of IPython <<<<<<<<')
#
# Then add the following line at the point in your code where
#   you want to inspect run­time values:
#
#       ipshell('some message to identify where we are')
#
# For more information see: http://ipython.scipy.org/moin/
#
#
# Constants
#

# AST node types
NoneNodeType = 0
ProgNodeType = 1
CommandNodeType = 2
FuncCallNodeType = 3
FuncCallListNodeType = 4
TermNodeType = 5

# Token types
NoneTokType = 0
LParTokType = 1
RParTokType = 2
WordTokType = 3
CommaTokType = 4
EOFTokType = 5

# Dictionary to map node type values to node type names
NodeTypeDict = {
    NoneNodeType: 'NoneNodeType',
    ProgNodeType: 'ProgNodeType',
    CommandNodeType: 'CommandNodeType',
    FuncCallNodeType: 'FuncCallNodeType',
    FuncCallListNodeType: 'FuncCallListNodeType',
    TermNodeType: 'TermNodeType',
}


# Representation of a node in the AST (abstract syntax tree).
class ASTNode:
    def __init__(self, nodeType, *args):
        self.nodeType = nodeType
        self.children = []
        for item in args:
            self.children.append(item)

    def show(self, level):
        self.showLevel(level)
        print 'Node -- Type %s' % NodeTypeDict[self.nodeType]
        level += 1
        for child in self.children:
            if isinstance(child, ASTNode):
                child.show(level)
            elif type(child) == types.ListType:
                for item in child:
                    item.show(level)
            else:
                self.showLevel(level)
                print 'Child:', child

    def showLevel(self, level):
        for idx in range(level):
            print '  ',


#
# The recursive descent parser class.
#   Contains the "recognizer" methods, which implement the grammar
#   rules (above), one recognizer method for each production rule.
#
class ProgParser:
    def __init__(self):
        pass

    def parseFile(self, infileName):
        self.infileName = infileName
        self.tokens = None
        self.tokenType = NoneTokType
        self.token = ''
        self.lineNo = -1
        self.infile = file(self.infileName, 'r')
        self.tokens = genTokens(self.infile)
        try:
            self.tokenType, self.token, self.lineNo = self.tokens.next()
        except StopIteration:
            raise RuntimeError, 'Empty file'
        result = self.prog_reco()
        self.infile.close()
        self.infile = None
        return result

    def parseStream(self, instream):
        self.tokens = genTokens(instream, '<instream>')
        try:
            self.tokenType, self.token, self.lineNo = self.tokens.next()
        except StopIteration:
            raise RuntimeError, 'Empty file'
            result = self.prog_reco()
            return result

    def prog_reco(self):
        commandList = []
        while 1:
            result = self.command_reco()
            if not result:
                break
            commandList.append(result)
        return ASTNode(ProgNodeType, commandList)

    def command_reco(self):
        if self.tokenType == EOFTokType:
            return None
        result = self.func_call_reco()
        return ASTNode(CommandNodeType, result)

    def func_call_reco(self):
        if self.tokenType == WordTokType:
            term = ASTNode(TermNodeType, self.token)
            self.tokenType, self.token, self.lineNo = self.tokens.next()
            if self.tokenType == LParTokType:
                self.tokenType, self.token, self.lineNo = self.tokens.next()
                result = self.func_call_list_reco()
                if result:
                    if self.tokenType == RParTokType:
                        self.tokenType, self.token, self.lineNo = \
                            self.tokens.next()
                        return ASTNode(FuncCallNodeType, term, result)
                    else:
                        raise ParseError(self.lineNo, 'missing right paren')
                else:
                    raise ParseError(self.lineNo, 'bad func call list')
            else:
                raise ParseError(self.lineNo, 'missing left paren')
        else:
            return None

    def func_call_list_reco(self):
        terms = []
        while 1:
            result = self.func_call_reco()
            if not result:
                break
            terms.append(result)
            if self.tokenType != CommaTokType:
                break
            self.tokenType, self.token, self.lineNo = self.tokens.next()
            return ASTNode(FuncCallListNodeType, terms)


#
# The parse error exception class.
#
class ParseError(Exception):
    def __init__(self, lineNo, msg):
        RuntimeError.__init__(self, msg)
        self.lineNo = lineNo
        self.msg = msg

    def getLineNo(self):
        return self.lineNo

    def getMsg(self):
        return self.msg


def is_word(token):
    for letter in token:
        if letter not in string.ascii_letters:
            return None
        return 1


#
# Generate the tokens.
# Usage:
#    gen = genTokens(infile)
#    tokType, tok, lineNo = gen.next()
#    ...
def genTokens(infile):
    lineNo = 0
    while 1:
        lineNo += 1
        try:
            line = infile.next()
        except:
            yield (EOFTokType, None, lineNo)

        toks = line.split()
        for tok in toks:
            if is_word(tok):
                tokType = WordTokType
            elif tok == '(':
                tokType = LParTokType
            elif tok == ')':
                tokType = RParTokType
            elif tok == ',':
                tokType = CommaTokType
            yield (tokType, tok, lineNo)


def test(infileName):
    parser = ProgParser()
    # ipshell('(test) #1\nCtrl­D to exit')
    result = None
    try:
        result = parser.parseFile(infileName)
    except ParseError, exp:
        sys.stderr.write('ParseError: (%d) %s\n' % \
                         (exp.getLineNo(), exp.getMsg()))
    if result:
        result.show(0)


def usage():
    print __doc__
    sys.exit(1)


def main():
    args = sys.argv[1:]
    try:
        opts, args = getopt.getopt(args, 'h', ['help'])
    except:
        usage()
    relink = 1
    for opt, val in opts:
        if opt in ('­h', '­­help'):
            usage()
    if len(args) != 1:
        usage()
    inputfile = args[0]
    test(inputfile)


if __name__ == '__main__':
    #import pdb; pdb.set_trace()
    main()
