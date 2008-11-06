#!/usr/bin/env python

## -*-Pyth-*-
 # ###################################################################
 #  FiPy - Python-based finite volume PDE solver
 # 
 #  FILE: "linearLUSolver.py"
 #
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
 #  
 # ###################################################################
 ##

__docformat__ = 'restructuredtext'

from fipy.tools import numerix

from fipy.solvers.scipy.scipySolver import ScipySolver

class LinearLUSolver(ScipySolver):
    """
    
    The `LinearLUSolver` solves a linear system of equations
    using LU-factorisation. This method solves systems of general
    non-symmetric matrices with partial pivoting.

    The `LinearLUSolver` is a wrapper class for the the SciPy_
    `scipy.linalg.lu_solve()` method.
    
    .. warning::

        Currently the solvers that use Scipy_ are only useful for
        small systems due to the whole sparse matrix having to be
        turned into an array of size N * N.
    
    .. _SciPy: http://www.scipy.org

    """
    
    def __init__(self, tolerance=1e-10, iterations=10, steps=None, precon=None):
        """
        Creates a `LinearScipyLUSolver`.

        :Parameters:
          - `tolerance`: The required error tolerance.
          - `iterations`: The number of LU decompositions to perform.
          - `steps`: A deprecated name for `iterations`.
            For large systems a number of iterations is generally required.

        """
        ScipySolver.__init__(self, tolerance=tolerance, iterations=iterations, steps=steps, precon=precon)

    def _solve(self, L, x, b):
        from scipy.linalg import lu_factor, lu_solve
    
##        x[:] = scipy.linalg.solve(numerix.array(L), b)
        LU = lu_factor(numerix.array(L))
        x[:] = lu_solve(LU, b)
        tol = self.tolerance + 1.

        for iteration in range(self.iterations):
            if tol <= self.tolerance:
                break

            errorVector = L * x - b
            LU = lu_factor(numerix.array(L))
            xError = lu_solve(LU, errorVector)
            x[:] = x - xError

            tol = max(numerix.absolute(xError))
            
            print tol