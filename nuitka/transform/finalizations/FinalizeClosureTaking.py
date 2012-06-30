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
""" Finalize the closure.

If a taker wants a variable, make sure that the closure taker in between all do forward it
for this use or else it will not be available. We do this late so it is easier to remove
closure variables and keep track of references, by not having it spoiled with these
transitive only references.

"""

from .FinalizeBase import FinalizationVisitorScopedBase

class FinalizeClosureTaking( FinalizationVisitorScopedBase ):
    def onEnterNode( self, node ):
        assert node.isClosureVariableTaker(), node

        # print node, node.provider

        for variable in node.getClosureVariables():
            referenced = variable.getReferenced()
            referenced_owner = referenced.getOwner()

            assert not referenced.isModuleVariable()

            current = node.getParent()

            # print referenced

            while current is not referenced_owner:
                if current.isClosureVariableTaker():
                    for current_variable in current.getClosureVariables():
                        if current_variable.getReferenced() is referenced:
                            break
                    else:
                        # print "ADD", current, referenced
                        current.addClosureVariable( referenced )


                current = current.getParent()
