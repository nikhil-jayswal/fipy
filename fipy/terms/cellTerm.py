#!/usr/bin/env python

## -*-Pyth-*-
 # ###################################################################
 #  FiPy - Python-based finite volume PDE solver
 # 
 #  FILE: "cellTerm.py"
 #                                    created: 11/12/03 {11:00:54 AM} 
 #                                last update: 6/10/04 {3:08:22 PM} 
 #  Author: Jonathan Guyer
 #  E-mail: guyer@nist.gov
 #  Author: Daniel Wheeler
 #  E-mail: daniel.wheeler@nist.gov
 #    mail: NIST
 #     www: http://ctcms.nist.gov
 #  
 # ========================================================================
 # This software was developed at the National Institute of Standards
 # and Technology by employees of the Federal Government in the course
 # of their official duties.  Pursuant to title 17 Section 105 of the
 # United States Code this software is not subject to copyright
 # protection and is in the public domain.  PFM is an experimental
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
 #  
 #  Description: 
 # 
 #  History
 # 
 #  modified   by  rev reason
 #  ---------- --- --- -----------
 #  2003-11-12 JEG 1.0 original
 # ###################################################################
 ##

import Numeric

from fipy.terms.term import Term
from fipy.tools.inline import inline

from fipy.tools.sparseMatrix import SparseMatrix

class CellTerm(Term):
    def __init__(self,weight,mesh):
	Term.__init__(self, mesh = mesh, weight = weight)

	self.diagCoeff = self.coeff * weight['diagonal']
	self.oldCoeff = self.coeff * weight['old value']
	self.bCoeff = self.coeff * weight['b vector']
	self.newCoeff = self.coeff * weight['new value']
	
    def _buildMatrixPy(self, L, oldArray, b, coeffScale, varScale, dt):
        N = len(oldArray)
        
	b += Numeric.array(oldArray) * self.oldCoeff[:] / (coeffScale * varScale) / dt
	b += Numeric.ones([N]) * self.bCoeff[:] / (coeffScale)
## 	L.update_add_pyarray(Numeric.ones([N]) * self.newCoeff[:]/coeffScale)
	L.addAtDiagonal(Numeric.ones([N]) * self.newCoeff[:]/coeffScale/dt)
        L.addAtDiagonal(Numeric.ones([N]) * self.diagCoeff[:]/coeffScale)

    def buildMatrix(self, oldArray, coeffScale, varScale, dt):
        coeffScale = coeffScale * varScale
        
        N = len(oldArray)
        b = Numeric.zeros((N),'d')
        L = SparseMatrix(size = N)

        inline.optionalInline(self._buildMatrixIn, self._buildMatrixPy, L, oldArray, b, coeffScale, varScale, dt)
        
        return (L, b)

    def _buildMatrixIn(self, L, oldArray, b, coeffScale, varScale, dt):

        if type(self.oldCoeff) is type(Numeric.zeros((2),'d')):
            oldCoeff = self.oldCoeff
            bCoeff = self.bCoeff
            newCoeff = self.newCoeff
            diagCoeff = self.diagCoeff
        else:
            oldCoeff = self.oldCoeff.getNumericValue()
            bCoeff = self.bCoeff.getNumericValue()
            newCoeff = self.newCoeff.getNumericValue()
            diagCoeff = self.diagCoeff.getNumericValue()
            
        if type(coeffScale) in (type(Numeric.zeros((2),'d')),type(1)):
            cScale = coeffScale
        else:
            cScale = coeffScale.getNumericValue()
        updatePyArray = Numeric.zeros((self.mesh.getNumberOfCells()),'d')
        inline.runInlineLoop1("""
            b(i) += oldArray(i) * oldCoeff(i) / coeffScale / varScale / dt;
            b(i) += bCoeff(i) / coeffScale;
            updatePyArray(i) += newCoeff(i) / coeffScale / dt;
            updatePyArray(i) += diagCoeff(i) / coeffScale;
        """,b = b[:],
            oldArray = oldArray.getNumericValue(),
            oldCoeff = oldCoeff,
            coeffScale = cScale,
            varScale = varScale.getNumericValue(),
            bCoeff = bCoeff,
            newCoeff = newCoeff,
            diagCoeff = diagCoeff,
            updatePyArray = updatePyArray[:],
            ni = len(updatePyArray[:]),
            dt = dt)

	L.addAtDiagonal(updatePyArray)

        
