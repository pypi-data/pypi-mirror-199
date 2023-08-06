import numpy as np
from irrep.gvectors import transformed_g 
import irrep.bandstructure as bs
from .util import cwd, R_to_spin, R_to_bvec
from .constants import Ry, a0, sx, sy, sz, alpha
from .qe_aux import read_espresso, read_kp_dat
from .lowdin import getHpowers, H_of_k

class irrep():
    '''
    A wrapper to call the routines from the irrep package:

    https://github.com/stepan-tsirkin/irrep/

    Additionally, we implement a modified version of the symm_matrix routine that
    allow us to calculate the matrix elements only within a selected list of bands,
    and adds a parameter to allow for anti-unitary operations, like time-reversal symmetry.
    '''
    def __init__(self,
            dftdir='.',
            outdir='.',
            #bandsgnu=None,
            #kpath=None,
            fWAV=None,
            fWFK=None,
            prefix=None,
            fPOS=None,
            Ecut=None,
            IBstart=None,
            IBend=None,
            kpt=None, # single kpt instead of kplist
            spinor=None,
            code='espresso',
            EF='auto',
            onlysym=False,
            spin_channel=None,
            refUC = None,
            shiftUC = None,
            identify_irreps = False,
            kname='',
            degen_thresh=1e-4
        ):
        '''
        Uses the irrep package to read the DFT data and calculates
        the matrix elements of the symmetry operations
        and the matrix elements of the momentum operator.

        Most of the parameters follow from the __init__() function
        of the class BandStructure from the bandstructure.py file
        of the irrep package. The only differences here are:

        Parameters
        ----------
        dftdir : str
            path point to the directory where the DFT data is stored
        outdir : str
            name of the directory informed as outdir to QE
        bandsgnu : str
            name of the band structure file in gnuplot format
        kpath=None,
            Number of points along each path and label of the k points used in QE 'bands' calculation.
            First line contains the number of points in each section of the k path, and the
            second line contains the labels of these k points. See example in read_dft.py.
        fWAV : see irrep package
        fWFK : see irrep package
        prefix : see irrep package
        fPOS : see irrep package
        Ecut : see irrep package
        IBstart : see irrep package
        IBend : see irrep package
        kpt : int
            Single number indicating the k point for the expansion.
            Equivalent to the kplist from the irrep package, but here
            it must be a single point.
        spinor : see irrep package
        code : see irrep package
        EF : see irrep package
        onlysym : see irrep package
        spin_channel : see irrep package
        refUC : see irrep package
        shiftUC : see irrep package
        identify_irreps : see irrep package
        kname : str
            label of the kpoint as defined in the irrep package
        degen_thresh : float
            threshold for the energy degeneracy

        Attributes
        ----------
        bandstr : object from the irrep BandStructure class
            The main irrep package object that stores the info
            read from the DFT data
        energies: array, shape(N,)
            Band energies in Rydberg units.
        symm_pg, symm_translation: list
            Poing group (S) and translation (T) components of the
            symmetry operation {S,T} (Seitz notation). See the
            comments in identify_symmetries() for more detail.
        irreps:
            List of degenerate bands with their irrep identification.
            Each entry contains [band indices, irreps list, degeneracy].
        antiU: list of arrays
            Matrix representations of the symmetry operators.
            Each line correspond to an operator. The first column
            refers to the matrix representation calculated from DFT,
            and the second column the one read from the QSYMM object. 
        px, py, pz : arrays
            matrices of the momentum operation along each 
            cartesian coordinate in in Bohr units
        GammaDFT : list of matrices 
            representations for each symmetry operation
        setA : list, slice
            stores the informed set A
        num_irreps: int
            number of irreps that compose set A
        alat : float
            the lattice constant in Bohr units
        fermi : float
            the Fermi energy in Ry units
        kpts : list
            list of k points used to define the plot axis
        klabels : list
            labels for each k point in kpts
        bands : array
            band structure data in gnuplot format
        '''
        kplist = np.ascontiguousarray(kpt)
        assert len(kplist) == 1, 'kpt should refer to a single k point.'

        # store paths and kpoint
        self.dftdir = dftdir
        self.prefix = prefix
        self.outdir = outdir
        self.kindex = kpt

        if code == 'espresso':
            self.alat, self.fermi = read_espresso(dftdir, prefix, outdir)
        else:
            raise Exception("Code not ready for " + code)

        # runs the irrep code on the outdir directory
        with cwd(dftdir + '/' + outdir):
            self.bandstr = bs.BandStructure(fWAV, fWFK, 
                                    prefix, fPOS, Ecut,
                                    IBstart, IBend, kplist,
                                    spinor, code, EF, onlysym, 
                                    spin_channel, refUC,
                                    shiftUC, identify_irreps)
        
        # extracts band energies and stores in a.u.
        self.energies = self.bandstr.kpoints[0].Energy / Ry - self.fermi
        # identify the symmetry operations
        self.symm_pg, self.symm_translation = self.identify_symmetries()
        # identify irreps
        self.irreps = self.get_irreps(kname, degen_thresh)
        # init list of anti-unitary symmetries
        self.antiU = []

    def fold_down_H(self, NB=None, maxorder=2):
        '''
        Uses Löwdin partitioning to calculate a dictionary
        with the matrices for each power of k.

        Example: key 'xx' refers to Hxx * k_x^2.
        
        The calculation is done in the crude, original QE basis.

        Parameters
        ----------
        NB : int or None
            Number of bands to consider the set B above set A.
        maxorder : int
            Maximum power of momentum.

        Properties
        ----------
        Hdict: Dictionary with the matrices that multiply the powers of momentum.

        '''
        self.Hdict = getHpowers(self, NB, maxorder)
    
    def build_H_of_k(self, all_bands=False):
        '''
        Builds a callable function Callable H(kx, ky, kz, [maxorder=2]).

        Parameters
        ----------
        all_bands = True/False
            If True, builds a first order model with all bands
            If False, builds the folded model for set A only up to maxorder
        
        Returns
        -------
        Callable H(kx, ky, kz, [maxorder=2])
        '''

        if all_bands:
            return H_of_k(self)
        else:
            return H_of_k(self, self.Hdict)


    def identify_symmetries(self):
        '''
        Reads the symmetry operations from the k point
        and stores it as human readable labels.

        Seitz notation {S,T}, where S is the point group part, 
        and T the translation part of the symmetry operation.

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
        symm_translation : list of arrays(float)
            Translation component of each symmetry operation
            in catesian coordinates.
        '''
        symm_pg = [] # label point group elements
        symm_translation = [] # label translations
        for op in self.bandstr.kpoints[0].symmetries:
            theop = [] # [pg, deg, axis], pg=(1,I,S,R,M)
            angle = round(np.rad2deg(op.angle))
            if angle == 0:
                if op.inversion:
                    theop = ['I', 0, [0,0,1]]
                else:
                    theop = ['1', 0, [0,0,1]]
            elif np.abs(angle) != 180:
                if op.inversion: # proto-rotation
                    theop = ['S', angle, list(np.round(op.axis, 2))]
                else: # rotation
                    theop = ['R', angle, list(np.round(op.axis, 2))]
            else: # angle = 180
                if op.inversion: # mirror
                    theop = ['M', 180, list(np.round(op.axis, 2))]
                else: # C2 rotation
                    theop = ['R', angle, list(np.round(op.axis, 2))]
            # store
            symm_pg += [theop]
            symm_translation += [np.round(op.translation, 2)]
        # return lists
        return symm_pg, symm_translation

    def get_irreps(self, kname='', degen_thresh=1e-4):
        '''
        Identify the irreps of each set of degenerate bands.

        Parameters
        ----------
        kname : str
            Label for the k point.
        degen_thresh : float
            Energy threshold (in eV) to identify degeneracies.
        
        Returns
        -------
        List of degenerate bands with their irrep identification.
        Each entry contains [band indices, irreps list, degeneracy].
        '''
        # get irrep tables for the k point
        irrep_tables = self.bandstr.spacegroup.get_irreps_from_table(kname, self.bandstr.kpoints[0].K)
        # run write_characters to get the jdata dict with the irreps
        # this code also creates the file irreps.dat, but we don't use it.
        _, _, _, jdata = self.bandstr.kpoints[0].write_characters(
            degen_thresh = degen_thresh,
            symmetries = [op.ind for op in self.bandstr.kpoints[0].symmetries],
            irreptable = irrep_tables)

        # reads jdata and stores only the necessary information
        # each entry has: band indices, irreps list, degeneracy
        irreps = []
        idb = 0
        for bnd,dim in zip(jdata['irreps'], jdata['dimensions']):
            txt = ''
            for key in bnd.keys():
                if bnd[key][0] > 0.3:
                    txt += '('+key+')'
            irreps.append([list(range(idb, idb+dim)), txt, dim])
            idb += dim

        return irreps
    
    def define_set_A(self, setA, verbose=True, NB=None, maxorder=2):
        '''
        Verifies if the chosen set A is composed by full sets of irreps.
        If not, it raises an error.
        
        If sucessful, defines set A and applies fold down.

        Parameters
        ----------
        setA : list, slice
            List of band indices to be used in the calculation.
        verbose: bool
            If true, prints information about the irreps from set A.
        NB : int or None
            Number of bands to consider the set B above set A.
        maxorder : int
            Maximum power of momentum.

        Attributes
        ----------
        setA : list, slice
            stores the informed set A
        num_irreps: int
            number of irreps that compose set A
        '''
        # print space group number and name
        if verbose:
            print('Space group ',
                    str(self.bandstr.spacegroup.number),
                    ':', self.bandstr.spacegroup.name)
            print('Group of the k-vector: <code not ready>')
            print('Verifying set A:', setA)

        # print report and store band indices
        # that match setA
        bandindices = []
        self.num_irreps = 0
        irreps_list = ''
        for ir in self.irreps: # band indices, irreps list, degeneracy
            if set(ir[0]) & set(setA):
                bandindices += ir[0]
                irreps_list += ir[1] # concatenate as string
                # irreps list has the structure: (-K7)(-K9)
                # the split of )( help us count the number of irreps in the list
                self.num_irreps += len(ir[1].split(')('))
                if verbose:
                    print('Band indices:', ir[0], 'Irreps:', ir[1], 'Degeneracy:', ir[2])

        # count occurrences of each irrep and 
        # calculate number of degrees of freedom (dog)
        # this will be the nullity in the basis transformation
        irreps_list = irreps_list[1:-1].split(')(') # remove (...) and split into list
        irreps_count = {} # init empty dict, entries are irreps
        for ir in irreps_list:
            if ir in irreps_count.keys():
                irreps_count[ir] += 1 # increment number of that irrep
            else:
                irreps_count[ir] = 1 # init if it is the first found
        # now calculate the dog = number of paramters in U(n) = n²
        # where n is the number of repeated irreps
        self.deg_of_freedom = 0
        for key in irreps_count.keys():
            self.deg_of_freedom += irreps_count[key]**2    
        
        # check if setA is complete
        if set(bandindices) != set(setA):
            raise Exception('Set A does not match a full set of irreps.')
        
        # store setA
        self.setA = setA

        # apply folding down
        self.fold_down_H(NB, maxorder)

    def get_symm_matrices(self, setA=None, store=True):
        '''
        Calculates the symmetry matrices of all operations of the k point,
        for the bands in set A.

        Parameters
        ----------
        setA : list, slice
            List of band indices to be used in the calculation.
        store : boolean
            If True, stores the matrices as an atribute of the object.
            If False, returns the matrices.
        
        Atributes / Returns
        -------------------
        GammaDFT : list of matrices for each symmetry operation
        '''
        if setA is None:
            setA = self.setA

        GammaDFT = []
        for op in self.bandstr.kpoints[0].symmetries:
            # calls our modified symm_matrix instead of the original
            # on of the irrep package
            GammaDFT += [symm_matrix(
                            self.bandstr.kpoints[0].K,
                            self.bandstr.kpoints[0].RecLattice, 
                            self.bandstr.kpoints[0].WF, 
                            self.bandstr.kpoints[0].ig, 
                            op.rotation, 
                            op.spinor_rotation, 
                            op.translation, 
                            op.spinor,
                            setA)]
        if store:
            self.GammaDFT = GammaDFT
        else:
            return GammaDFT

    def get_p_matrices(self, setA=slice(None), SOC=False, qekp=''):
        '''
        Calculates the matrices of the momentum operator in Bohr units
        for the bands in set A.

        Parameters
        ----------
        setA : list, slice
            List of band indices to be used in the calculation.
        SOC : boolean
            If True, estimates p_soc and calculates sigma matrices
        qekp : str
            Name of the QE file with the matrix elements of p
        
        Atributes / Returns
        -------------------
        px, py, pz : matrices of the momentum operation along each 
                     cartesian coordinate in in Bohr units
        '''

        if qekp != '': # read p from kp.dat
            kpdat = self.dftdir + '/' + qekp
            aux = read_kp_dat(kpdat)
            self.px = np.copy(aux.p1)
            self.py = np.copy(aux.p2)
            self.pz = np.copy(aux.p3)
            del aux
        else: # do no use kp.dat, calculate p from plane-waves
            # reciprocal lattice vector in Bohr units
            # RecLattice is in 1/Angstrom, 
            # so we multiply by 10*a0 = 0.529177249 [Angstrom]
            bvec = self.bandstr.RecLattice * (10*a0)
            self.px = p_matrix(self.bandstr.kpoints[0].K, bvec, self.bandstr.kpoints[0].WF, self.bandstr.kpoints[0].ig, self.bandstr.spinor, 0, setA)
            self.py = p_matrix(self.bandstr.kpoints[0].K, bvec, self.bandstr.kpoints[0].WF, self.bandstr.kpoints[0].ig, self.bandstr.spinor, 1, setA)
            self.pz = p_matrix(self.bandstr.kpoints[0].K, bvec, self.bandstr.kpoints[0].WF, self.bandstr.kpoints[0].ig, self.bandstr.spinor, 2, setA)

        if SOC: # estimate SOC and sigma matrices
            # matrix elements of sigma <m|sigma|n>
            self.sigma_x = sigma_matrix(self.bandstr.kpoints[0].WF, self.bandstr.kpoints[0].ig, self.bandstr.spinor, sx, setA)
            self.sigma_y = sigma_matrix(self.bandstr.kpoints[0].WF, self.bandstr.kpoints[0].ig, self.bandstr.spinor, sy, setA)
            self.sigma_z = sigma_matrix(self.bandstr.kpoints[0].WF, self.bandstr.kpoints[0].ig, self.bandstr.spinor, sz, setA)

            # aux function: <m|s_mu . V_nu|n>
            sV = lambda s, p: 1j*(np.einsum('n,mj,jn->mn',self.energies, s, p) - np.einsum('j,mj,jn->mn',self.energies, s, p))
            # <m|psoc_x|n> = (α²/8) (σy.Vz - σz.Vy)
            # <m|psoc_y|n> = (α²/8) (σz.Vx - σx.Vz)
            # <m|psoc_z|n> = (α²/8) (σx.Vy - σy.Vx)
            self.psoc_x = ((alpha**2)/8) * (sV(self.sigma_y, self.pz) - sV(self.sigma_z, self.py))
            self.psoc_y = ((alpha**2)/8) * (sV(self.sigma_z, self.px) - sV(self.sigma_x, self.pz))
            self.psoc_z = ((alpha**2)/8) * (sV(self.sigma_x, self.py) - sV(self.sigma_y, self.px))

    def add_antiunitary_symm(self, QS, T, bands=None):
        '''
        Calculates symmetry matrix S_mn = <Psi_m|{A|T}|Psi_n>
        assuming that that the symmetry is anti-unitary and 
        applies the complex conjugate on the <Psi_m|.

        Parameters
        ----------
        QS : QSYMM object
            The correspoding symmetry as a QSYMM object.
        T : array, shape=(3,)
            Translational part of the symmetry operation, in terms of the basis 
            vectors of the unit cell.
        bands : slice, list, array, shape=(N,)
            Selects which bands (m,n) will be used in the calculation.

        Attributes
        ----------
        antiU: list of arrays (N,N)
            Matrix representations of the symmetry operators.
            Each line correspond to an operator. The first column
            refers to the matrix representation calculated from DFT,
            and the second column the one read from the QSYMM object.    
        '''
        if bands == None:
            bands = self.setA

        # convert R to reciprocal space and to spin space
        A = R_to_bvec(QS.R, self.bandstr.kpoints[0].RecLattice)
        S = R_to_spin(QS.R)
        # multiplies by TRS
        S = 1j*sy @ S
        # calculate U
        U = symm_matrix(self.bandstr.kpoints[0].K,
                        self.bandstr.kpoints[0].RecLattice, 
                        self.bandstr.kpoints[0].WF, 
                        self.bandstr.kpoints[0].ig, 
                        A, S, T, self.bandstr.spinor, bands, True)
        # add to list of antiU
        self.antiU += [[U, QS.U]]


##################################################
# MODIFIED VERSIONS OF THE symm_matrix ROUTINE   #
# FROM THE gvectors.py FILE OF THE IRREP PACKAGE #
##################################################

def p_matrix(K, RecLattice, WF, igall, spinor, xyz, bands=slice(None)):
    '''
    Calculates the matrix elements of the momentum operator <m|p_nu|n> along
    direction nu=xyz.

    This routine is based on the symm_matrix routine from the irrep package (gvectors.py).
    
    Parameters
    ----------
    K : array, shape=(3,)
        Direct coordinates of the k-point.
    RecLattice : array, shape=(3,3)
        Each row contains the cartesian coordinates of a basis vector forming 
        the unit-cell in reciprocal space.
    WF : array
        `WF[i,j]` contains the coefficient corresponding to :math:`j^{th}`
        plane-wave in the expansion of the wave-function in :math:`i^{th}`
        band. It contains only plane-waves if energy smaller than `Ecut`.
    igall : array
        Returned by `__sortIG`.
        Every column corresponds to a plane-wave of energy smaller than 
        `Ecut`. The number of rows is 6: the first 3 contain direct 
        coordinates of the plane-wave, the fourth row stores indices needed
        to short plane-waves based on energy (ascending order). Fitfth 
        (sixth) row contains the index of the first (last) plane-wave with 
        the same energy as the plane-wave of the current column.
    spinor : bool
        `True` if wave functions are spinors, `False` if they are scalars.
    xyz : int
        Values 0, 1, 2 refer to the cartesian coordinates x, y, z.
    bands : slice, list, array, shape=(N,)
        Selects which bands (m,n) will be used in the calculation.

    Returns
    -------
        Matrix of the momentum operator in the basis of eigenstates of the 
        Bloch Hamiltonian :math:`H(k)`.
    '''
    npw = igall.shape[1]
    WF = WF[bands] # local copy if sliced, original (copy by reference) if not sliced
    if spinor:
        WF = np.stack([WF[:, :npw], WF[:, npw:]], axis=2)
        return np.einsum("mgs,ngs,ig,i->mn", WF.conj(), WF, igall[:3,:] + K[:, None], RecLattice[:,xyz])
    else:
        return np.einsum("mg ,ng ,ig,i->mn", WF.conj(), WF, igall[:3,:] + K[:, None], RecLattice[:,xyz])

def symm_matrix(K, RecLattice, WF, igall, A, S, T, spinor, bands=slice(None), TRS=False):
    """
    Modifies the original symm_matrix routine from the irrep package (gvectors.py).
    The original routine computes the matrix S_mn = <Psi_m|{A|T}|Psi_n>.
    Here we add two parameters: bands and TRS.

    The bands parameter controls which bands will be used in the calculation.
    The default is to use all bands.

    If TRS == True the code assumes that the symmetry operation is anti-unitary,
    adding the complex conjugation to the symmetry operation, acting to the left.

    Parameters
    ----------
    K : array, shape=(3,)
        Direct coordinates of the k-point.
    RecLattice : array, shape=(3,3)
        Each row contains the cartesian coordinates of a basis vector forming 
        the unit-cell in reciprocal space.
    WF : array
        `WF[i,j]` contains the coefficient corresponding to :math:`j^{th}`
        plane-wave in the expansion of the wave-function in :math:`i^{th}`
        band. It contains only plane-waves if energy smaller than `Ecut`.
    igall : array
        Returned by `__sortIG`.
        Every column corresponds to a plane-wave of energy smaller than 
        `Ecut`. The number of rows is 6: the first 3 contain direct 
        coordinates of the plane-wave, the fourth row stores indices needed
        to short plane-waves based on energy (ascending order). Fitfth 
        (sixth) row contains the index of the first (last) plane-wave with 
        the same energy as the plane-wave of the current column.
    A : array, shape=(3,3)
        Matrix describing the tranformation of basis vectors of the 
        reciprocal space vectors b_i
    S : array, shape=(2,2)
        Matrix describing how spinors transform under the symmetry.
    T : array, shape=(3,)
        Translational part of the symmetry operation, in terms of the basis 
        vectors of the unit cell.
    spinor : bool
        `True` if wave functions are spinors, `False` if they are scalars.
    bands : slice, list, array, shape=(N,)
        Selects which bands (m,n) will be used in the calculation.
    TRS : bool, default = False
        If True, adds the complex conjugation to the symmetry operation.
    
    Returns
    -------
    array
        Matrix of the symmetry operation in the basis of eigenstates of the 
        Bloch Hamiltonian :math:`H(k)`.
    """
    npw = igall.shape[1]
    TRS_sign = (-1)**TRS # 1 if False, -1 if True
    multZ = np.exp(-1.0j * (2 * np.pi * A.dot(T).dot(igall[:3, :] + K[:, None])))
    igrot = transformed_g(K, igall, RecLattice, TRS_sign*A)
    WF = WF[bands] # local copy if sliced, original (copy by reference) if not sliced
    if spinor:
        WF1 = np.stack([WF[:, igrot], WF[:, igrot + npw]], axis=2).conj()
        WF2 = np.stack([WF[:, :npw], WF[:, npw:]], axis=2)
        if TRS:
            WF1 = WF1.conj()
        return np.einsum("mgs,ngt,g,st->mn", WF1, WF2, multZ, S)
    else:
        if TRS:
            return np.einsum("mg,ng,g->mn", WF[:, igrot], WF, multZ)
        else:
            return np.einsum("mg,ng,g->mn", WF[:, igrot].conj(), WF, multZ)


def sigma_matrix(WF, igall, spinor, sigma, bands=slice(None)):
    '''
    Calculates the matrix elements of the momentum operator <m|sigma_nu|n> along
    direction nu=xyz.

    This routine is based on the symm_matrix routine from the irrep package (gvectors.py).
    
    Parameters
    ----------
    WF : array
        `WF[i,j]` contains the coefficient corresponding to :math:`j^{th}`
        plane-wave in the expansion of the wave-function in :math:`i^{th}`
        band. It contains only plane-waves if energy smaller than `Ecut`.
    igall : array
        Returned by `__sortIG`.
        Every column corresponds to a plane-wave of energy smaller than 
        `Ecut`. The number of rows is 6: the first 3 contain direct 
        coordinates of the plane-wave, the fourth row stores indices needed
        to short plane-waves based on energy (ascending order). Fitfth 
        (sixth) row contains the index of the first (last) plane-wave with 
        the same energy as the plane-wave of the current column.
    spinor : bool
        `True` if wave functions are spinors, `False` if they are scalars.
    sigma : array
        Pauli matrix sigma_x/y/z.
    bands : slice, list, array, shape=(N,)
        Selects which bands (m,n) will be used in the calculation.

    Returns
    -------
        Matrix of the momentum operator in the basis of eigenstates of the 
        Bloch Hamiltonian :math:`H(k)`.
    '''
    npw = igall.shape[1]
    WF = WF[bands] # local copy if sliced, original (copy by reference) if not sliced
    if spinor:
        WF = np.stack([WF[:, :npw], WF[:, npw:]], axis=2)
        return np.einsum("mgs,st,ngt->mn", WF.conj(), sigma, WF)
    else:
        raise Exception('Sigma matrix elements not defined for spinles case.')