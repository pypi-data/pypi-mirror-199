from numpy import fromstring, append
from qsymm.groups import pretty_print_pge
from qsymm import continuum_hamiltonian, display_family
from qsymm import inversion, rotation, mirror, time_reversal, PointGroupElement
from qsymm.model import _commutative_momenta
from qsymm.hamiltonian_generator import hamiltonian_from_family
from .util import convertpi

class qsymm():
    '''
    This module is a wrapper to call routines from the qsymm package:

    https://github.com/quantum-tinkerer/qsymm

    The class stores the information needed to:
    
    - Calculate the Kane and Luttinger parameters
    - Rotate the DFT basis to match the representations informed here.
    '''

    def __init__(self,
                 # parameters from continuum_hamiltonian(...)
                 symmetries, 
                 dim, 
                 total_power, 
                 all_powers=None, 
                 momenta=_commutative_momenta,
                 sparse_linalg=False, 
                 prettify=True, 
                 num_digits=10,
                 # extra parameter: print model or not?
                 print_model=True,
                 # parameters from display_family(...)
                 summed=True,
                 coeffs=None,
                 nsimplify=True
                 ):
        '''
        Uses the qsymm package to build a kp model.
        Most of the input parameters of __init__() follow 
        from the qsymm routines:
        
        - continuum_hamiltonian(...)
        - display_family(...)

        Additionally, we add the parameter print_model to define
        whether or not to call display_family(...).

        Parameters
        ----------
        symmetries : see qsymm package
        dim : see qsymm package
        total_power : see qsymm package
        all_powers : see qsymm package
        momenta : see qsymm package
        sparse_linalg : see qsymm package
        prettify : see qsymm package
        num_digits : see qsymm package
        print_model : bool
            If the user wants to call display_family(...) when generating the model.
        summed : see qsymm package
        coeffs : see qsymm package
        nsimplify : see qsymm package

        Attributes
        ----------
        symms : list
            The symmetries built with qsymm
        model : list
            List of qsymm/Model objects with the matrices
            that define the kp model
        symm_pg: list
            Poing group (S) component of the
            symmetry operation {S,T} (Seitz notation). See the
            comments in identify_symmetries() for more detail.
        '''

        self.symms = symmetries
        self.model = continuum_hamiltonian(symmetries,
                                           dim, 
                                           total_power, 
                                           all_powers, 
                                           momenta,
                                           sparse_linalg, 
                                           prettify, 
                                           num_digits)
        
        self.Hmodel = hamiltonian_from_family(self.model)
        
        self.symm_pg = self.identify_symmetries()
        
        if print_model:
            display_family(self.model, summed, coeffs, nsimplify)



    def identify_symmetries(self):
        '''
        Reads the symmetry operations and identifies their
        point group parts. There's no information about
        non-symmorphic translations, since these are implied
        in the U matrices.

        Returns
        -------
        symm_pg : list
            Each element describes the point group (S) part of the
            symmetry operation. Each entry has three components.
            The first component (string) identifies the type of operation:
            1 for identity, I for inversion, S for proto-rotation,
            C for rotation, M for mirror. 
            The second entry (int) is the angle (degrees). 
            For I and 1 we use angle = 0, and for M the angle is 180. 
            The third entry is the axis (array, shape (3,), float).
            For I and 1 we use [0,0,1]. For C and S it is the
            rotation axis, and for M it is the normal to the mirror plane.
            In all cases the axis are in cartesian coordinates.
        '''
        # [(1,I,S,R,M), deg, axis]
        # if conjugate, adds T label
        symm_pg = []
        for n in range(len(self.symms)):
            opstr = pretty_print_pge(self.symms[n])
            TRS = ''
            if self.symms[n].conjugate:
                TRS = 'T'
            if (opstr[0] == '1') or (opstr[0] == 'I'):
                theop = [TRS+opstr[0], 0, [0,0,1.]]
            elif (opstr[0] == 'R') or (opstr[0] == 'S'):
                theop = [TRS+opstr[0]] # label R or S
                if ',' in opstr: # 3D case as R(angle, axis)
                    opstr = opstr[2:-1].split(',') # angle,axis
                    angle = convertpi(opstr[0])
                    theax = opstr[1].strip()
                    theax = fromstring(theax[1:-1], sep=' ')                        
                    theop += [angle, list(theax)]
                else: # 2D case as R(angle), while axis is assumed [0,0,1]
                    angle = convertpi(opstr[2:-1])
                    theop += [angle, [0,0,1]]
            else: # M(axis)
                theax = opstr[2:-1].strip()
                theax = fromstring(theax[1:-1], sep=' ')
                # add zero if 2D
                if len(theax) == 2: theax = append(theax, 0)
                theop = [TRS+opstr[0], 180, list(theax)]
            # store
            symm_pg += [theop]
        # return list
        return symm_pg
    
