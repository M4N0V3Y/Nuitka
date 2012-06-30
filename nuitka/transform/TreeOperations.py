#     Copyright 2012, Kay Hayen, mailto:kayhayen@gmx.de
#
#     Part of "Nuitka", an optimizing Python compiler that is compatible and
#     integrates with CPython, but also works on its own.
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
#
""" Operations on the tree.

This is mostly for the different kinds of visits that the node tree can have. You
can visit a scope, a tree (module), every scope of a tree (module) and the whole
forest of modules.

"""

class ExitNodeVisit( BaseException ):
    pass

class ExitVisit( BaseException ):
    pass

class RestartVisit( BaseException ):
    pass

def _visitTree( tree, visitor, limit_tag ):
    try:
        visitor.onEnterNode( tree )

        visit_children = True
    except ExitNodeVisit:
        visit_children = False

    if visit_children:
        for visitable in tree.getChildNodesNotTagged( limit_tag ):
            if visitable is None:
                raise AssertionError( "'None' child encountered", tree, tree.source_ref )

            _visitTree( visitable, visitor, limit_tag )

    visitor.onLeaveNode( tree )

def visitTree( tree, visitor, limit_tag = None ):
    try:
        _visitTree( tree, visitor, limit_tag )
    except ExitVisit:
        pass
    except RestartVisit:
        visitTree( tree, visitor, limit_tag )

def visitScope( tree, visitor ):
    visitTree( tree, visitor, "closure_taker" )


def visitScopes( tree, visitor ):
    class VisitEverything( VisitorNoopMixin ):
        def onEnterNode( self, node ):
            if node.hasTag( "closure_taker" ):
                visitor.onEnterScope( node )
                visitTree( node, visitor, "closure_taker" )
                visitor.onLeaveScope( node )

    _visitTree( tree, VisitEverything(), None )

def visitTagHaving( tree, visitor, tag ):
    class VisitEverything( VisitorNoopMixin ):
        def onEnterNode( self, node ):
            if node.hasTag( tag ):
                visitor.onEnterNode( node )

    _visitTree( tree, VisitEverything(), None )


class VisitorNoopMixin:
    def onEnterNode( self, node ):
        """ To be optionally overloaded for operation before the node children were done. """
        pass

    def onLeaveNode( self, node ):
        """ To be optionally overloaded for operation after the node children were done. """
        pass

    # Only for "scope" and "execution" visits.
    def onEnterScope( self, tree ):
        """ To be optionally overloaded for per-scope entry tasks. """
        pass

    def onLeaveScope( self, tree ):
        """ To be optionally overloaded for per-scope exit tasks. """
        pass
