#!/usr/bin/env python

## 
 # ###################################################################
 #  FiPy - Python-based finite volume PDE solver
 # 
 #  FILE: "test.py"
 #                                    created: 11/10/03 {3:23:47 PM}
 #                                last update: 7/13/05 {3:30:55 PM} 
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
 #  Description: 
 # 
 #  History
 # 
 #  modified   by  rev reason
 #  ---------- --- --- -----------
 #  2003-11-10 JEG 1.0 original
 # ###################################################################
 ##

import unittest
import fipy.tests.testProgram

from fipy.models.phase.theta.modularVariable import ModularVariable
from fipy.tools import numerix
from fipy.tools.numerix import pi
from fipy.meshes.grid2D import Grid2D
from fipy.tests.testBase import _TestBase
from fipy.models.phase.theta.noModularVariable import _NoModularVariable

class TestMod(_TestBase):
    def setUp(self, value, dx = 1., dy = 1.):
        self.mesh = Grid2D(dx = dx, dy = dy, nx = 2, ny = 1)
        self.theta = ModularVariable(
            mesh = self.mesh,
            value = value)

    def testResult(self):
        self.assertArrayWithinTolerance(self.result, self.answer, 1e-10)

class TestModFace(TestMod):
    def setUp(self, value, dx = 1., dy = 1.):
        TestMod.setUp(self, value, dx = dx, dy = dy)

    def reorderResult(self):
        interiorIDs =  self.mesh.getInteriorFaceIDs()
        exteriorIDs = self.mesh.getExteriorFaceIDs()
        self.result = numerix.take(self.result, numerix.concatenate((interiorIDs, exteriorIDs)))

class TestModSubtract(TestMod):
    def setUp(self):
        TestMod.setUp(self, -2 * pi / 3.)
        self.thetaOther = ModularVariable(
            mesh = self.theta.getMesh(),
            value = 2. * pi / 3.)
##        print self.thetaOther
##        print self.theta
##        print "going into the subtraction"
##        print self.thetaOther - self.theta
##        raw_input()
        self.result = (self.thetaOther - self.theta).getNumericValue()
        self.answer = self.theta.getNumericValue()

class TestModCellToFace(TestModFace):
    def setUp(self):
        TestMod.setUp(self, numerix.array((2. * pi / 3., -2. * pi / 3. )))
        self.answer = numerix.array((-pi, 2. * pi / 3., -2. * pi / 3., 2. * pi / 3., -2. * pi / 3., 2. * pi / 3., -2. * pi / 3. ))
        self.result = self.theta.getArithmeticFaceValue().getNumericValue()
        self.reorderResult()
        
class TestModCellGrad(TestMod):
    def setUp(self):
        dx = 0.5
        TestMod.setUp(self, numerix.array((2. * pi / 3., -2. * pi / 3.)), dx = dx, dy = 0.5)
        self.answer = numerix.array(((pi / 3., 0.), (pi / 3., 0.))) / dx
        self.result = self.theta.getGrad().getNumericValue()

class TestModNoMod(TestMod):
    def setUp(self):
        TestMod.setUp(self, 1., dx = 1., dy = 1.)
        thetaNoMod = _NoModularVariable(self.theta)
        self.answer = numerix.array((0. , 0.))
        self.theta[:] = self.answer
        self.result = thetaNoMod.getNumericValue()

class TestModFaceGrad(TestModFace):
    def setUp(self):
        dx = 0.5
        dy = 0.5
        TestModFace.setUp(self, numerix.array((2. * pi / 3., -2. * pi / 3.)) , dx = dx, dy = dy)
        self.answer = numerix.array(((2. * pi / 3., 0.), (pi / 3., 0.), (pi / 3., 0.), (pi / 3., 0.), (pi / 3., 0.), (0., 0.), (0., 0.))) / dx
        self.result = self.theta.getFaceGrad().getNumericValue()
        self.reorderResult()

class TestModFaceGradNoMod(TestModFace):
    def setUp(self):
        dx = 0.5
        dy = 0.5
        TestModFace.setUp(self, numerix.array((2. * pi / 3., -2. * pi / 3.)) , dx = dx, dy = dy)
        thetaNoMod = _NoModularVariable(self.theta)
        self.answer = numerix.array(((2. * pi / 3., 0.), (pi / 3., 0.), (pi / 3., 0.), (pi / 3., 0.), (pi / 3., 0.), (0., 0.), (0., 0.))) / dx - numerix.array(((-4. * pi / 3., 0.), (-2. * pi / 3., 0.), (-2. * pi / 3., 0.), (-2. * pi / 3., 0.), (-2. * pi / 3., 0.), (0., 0.), (0., 0.))) / dx
        self.diff = self.theta.getFaceGrad() - thetaNoMod.getFaceGrad()
        self.result = self.diff.getNumericValue()
        self.reorderResult()
        
class TestModFaceGradNoMod1(TestModFaceGradNoMod):
    def setUp(self):
        TestModFaceGradNoMod.setUp(self)
        self.theta.setValue(numerix.array((0., -2 * pi / 3.)))
        self.answer = numerix.array(((0., 0.), (0., 0.), (0., 0.), (0., 0.), (0., 0.), (0., 0.), (0., 0.)))
        self.result =  self.diff.getNumericValue()
        self.reorderResult()
        
def _suite():
    theSuite = unittest.TestSuite()
    theSuite.addTest(unittest.makeSuite(TestModSubtract))
    theSuite.addTest(unittest.makeSuite(TestModCellToFace))
    theSuite.addTest(unittest.makeSuite(TestModCellGrad))
    theSuite.addTest(unittest.makeSuite(TestModNoMod))
    theSuite.addTest(unittest.makeSuite(TestModFaceGrad))
    theSuite.addTest(unittest.makeSuite(TestModFaceGradNoMod))
    theSuite.addTest(unittest.makeSuite(TestModFaceGradNoMod1))
    return theSuite
    
if __name__ == '__main__':
    fipy.tests.testProgram.main(defaultTest='_suite')
