#!/usr/bin/env python

## -*-Pyth-*-
 # ###################################################################
 #  FiPy - Python-based finite volume PDE solver
 # 
 #  FILE: "callBackCellToFaceVariable.py"
 #                                    created: 2/20/04 {11:15:10 AM} 
 #                                last update: 5/18/06 {8:38:53 PM} 
 #  Author: Jonathan Guyer <guyer@nist.gov>
 #  Author: Daniel Wheeler <daniel.wheeler@nist.gov>
 #  Author: James Warren   <jwarren@nist.gov>
 #    mail: NIST
 #     www: http://www.ctcms.nist.gov/fipy/
 #  
 # ========================================================================
 # This software was developed at the National Institute of Standards
 # and Technology by employees of the Federal Government in the course
 # of their official duties.  Pursuant to title 17 Section 105 of the
 # United States Code this software is not subject to copyright
 # protection and is in the public domain.  FiPy is an experimental
 # system.  NIST assumes no responsibility whatsoever for its use by
 # other parties, and makes no guarantees, expressed or implied, about
 # its quality, reliability, or any other characteristic.  We would
 # appreciate acknowledgement if the software is used.
 # 
 # This software can be redistributed and/or modified freely
 # provided that any derivative works bear some notice that they are
 # derived from it, and any modified versions bear some notice that
 # they have been modified.
 # ========================================================================
 #  See the file "license.terms" for information on usage and  redistribution
 #  of this file, and for a DISCLAIMER OF ALL WARRANTIES.
 #  
 # ###################################################################
 ##

from fipy.variables.cellToFaceVariable import _CellToFaceVariable
from fipy.tools import numerix

class _CallBackCellToFaceVariable(_CellToFaceVariable):
    def __init__(self, var, func):
        _CellToFaceVariable.__init__(self, var)
        self.func = func
        
    def _calcValuePy(self, alpha, id1, id2):
        cell1 = numerix.take(self.var,id1)
        cell2 = numerix.take(self.var,id2)
        return self.func(cell1, cell2)

    _calcValueIn = _calcValuePy
    