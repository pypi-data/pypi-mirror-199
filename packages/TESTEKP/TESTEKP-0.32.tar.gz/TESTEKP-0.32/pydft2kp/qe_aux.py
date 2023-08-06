from numpy import loadtxt, pi, array, where, fromstring, unique, argwhere, copy
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
from .constants import Ry, a0

class qe_plotter:

    def __init__(self, kp, bandsgnu, kpath):
        # extract info from kp object
        dftdir = kp.dftdir
        outdir = kp.outdir
        prefix = kp.prefix
        alat = kp.alat
        fermi = kp.fermi
        kpt = kp.kindex
        
        # energy list at the k point
        self.en_at_k = kp.energies

        # kpaths and labels for k axis
        # and bands for plotting
        # kpt -> kpt-1 because python starts at 0
        self.kpaths, self.klabels, data = qe_bands_fix_units(dftdir, bandsgnu, kpath, kpt-1, alat, fermi)
        self.kdist = unique(data[:,0]) # the k axis as distances = 1D path
        nk = len(self.kdist)
        ne = data.shape[0]//nk
        self.bands = data[:,1].reshape([ne,nk]).T # the energy data

        # read the 3D version of k axis
        xmlpath = dftdir + '/' + outdir + '/' + prefix + '.xml'
        xmlroot = ET.parse(xmlpath).getroot()
        kpts = xmlroot.find('input').find('k_points_IBZ').findall('k_point')
        self.k3D = []
        for each in kpts:
            self.k3D += [fromstring(each.text, sep=' ')]
        self.k3D = array(self.k3D) * 2*pi/alat # fix units
        self.k3D -= self.k3D[kpt-1] # shift central k to origin
    
    def set_labels_and_limits(self, ax, xmin=None, xmax=None, ymin=None, ymax=None):
        # set y label
        ax.set_ylabel(R"Energy [Ry]")
        # set limits
        if xmin is None: xmin = self.kdist[0]
        if xmax is None: xmax = self.kdist[-1]
        if ymin is None: ymin = -1
        if ymax is None: ymax = +1
        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)

        klabels = list(copy(self.klabels))
        kpaths = list(copy(self.kpaths))

        # adjust xmin labels if needed
        idx = argwhere(array(kpaths) < xmin)
        if len(idx) > 0:
            idx = idx[-1][0]
            klabels[idx] = klabels[idx] + r'$\leftarrow$'
            kpaths[idx] = xmin
        # the same for xmax
        idx = argwhere(array(kpaths) > xmax)
        if len(idx) > 0:
            idx = idx[0][0]
            klabels[idx] = r'$\rightarrow$' + klabels[idx]
            kpaths[idx] = xmax
        
        # set x labels
        ax.set_xticks(kpaths, klabels)
        ticklabels = ax.get_xticklabels()
        ticklabels[ 0].set_ha("left")
        ticklabels[-1].set_ha("right")


def qe_bands_fix_units(dftdir, bandsgnu, kpath, kpt, alat, fermi):
    '''
    Reads bands in gnuplot format.
    The bands data is adjusted to set the Fermi energy at zero, and
    express the k points in Bohr units (2pi/alat).

    Parameters
    ----------
    dftdir : str
        Directory where the QE data is stored
    bandsgnu : str
        Name of the file with the bands in gnuplot format
    kpath : array(2, 3)
        Number of points along each path and label of the k points used in QE 'bands' calculation.
        First line contains the number of points in each section of the k path, and the
        second line contains the labels of these k points. See example below.
    kpt : int
        Index of the cenral k point selected for the kp expansion.
    alat : float
        The lattice parameter in Bohr units.
    fermi : float
        The Fermi energy in Ry units.
    
    Returns
    -------
    kpts : array, int
        Indexes of the k points along the path.
    klabels : array, str
        Label of the k points along the path.
    data : array, float
        The k points and energies from the gnuplot file.

    Examples
    --------

    To understand the paths informed here, consider the following three:
    .
    ├── your_python_code.ipynb
    ├── ...
    └──dftdata
        ├─── bands.gnu
        ├── ...
        └─── outdir
                ├── ...
                └──── graphene.save
                        ├── ...
                        └──── data-file-schema.xml

    This implies these parameters:
        dftdir = 'dftdata'
        prefix = 'graphene'
        outdir = 'outdir'
        bandsgnu = 'bands.gnu'

    To understand the kpath parameter, consider that the QE bands calculation
    is set with the following K_POINTS namelist

        K_POINTS crystal_b
        3
        +0.0000000000 0.000000000 0.000000000 30 ! G
        +0.3333333333 0.333333333 0.000000000 40 ! K
        +0.0000000000 0.500000000 0.000000000  1 ! M

    The path from G to K contain 30 point, and from K to M 40 points.
    The last number (1) in the M line is irrelevant. The first line
    of kpath must inform these numbers: [30, 40, 1]. The second line
    of kpath must have the labels for these k points.
    It can be simple strings, as ['G', 'K', 'M'], or Latex formated
    strings as [R'$\Gamma$', R'$K$', R'$M$']. So, here we get

    kpath = [[30, 40, 1], [R'$\Gamma$', R'$K$', R'$M$']]
    '''

    bandspath = dftdir + '/' + bandsgnu
    
    # example: kpath = [[30, 30, 30], [R'$\Gamma$', R'$K$', R'$M$']]
    klabels = kpath[1] # example: [R'$\Gamma$', R'$K$', R'$M$']
    kids = [0]
    for klen in kpath[0][:-1]:
        kids.append(kids[-1]+klen) # example: [0, 30, 60]

    # READ DFT BANDS
    data = loadtxt(bandspath)
    data[:,0] -= data[kpt,0]
    data[:,0] *= 2*pi/alat # fix units
    data[:,1] /= Ry
    data[:,1] -= fermi # sets Fermi energy at 0
    # set k path and labels for the plots
    kpts = [data[k,0] for k in kids]

    return kpts, klabels, data

def read_espresso(dftdir, prefix, outdir):
    '''
    Reads QE data: alat, Fermi energy.

    Parameters
    ----------
    dftdir : str
        Directory where the QE data is stored
    prefix : str
        Prefix used in the QE calculation
    outdir : str
        Outdir used in the QE calculation
    
    Returns
    -------
    alat : float
        The lattice parameter in Bohr units.
    fermi : float
        The Fermi energy in Ry units.
    
    Examples
    --------

    To understand the paths informed here, consider the following three:
    .
    ├── your_python_code.ipynb
    ├── ...
    └──dftdata
        ├─── bands.gnu
        ├── ...
        └─── outdir
                ├── ...
                └──── graphene.save
                        ├── ...
                        └──── data-file-schema.xml

    This implies these parameters:
        dftdir = 'dftdata'
        prefix = 'graphene'
        outdir = 'outdir'
        bandsgnu = 'bands.gnu'
    '''

    xmlpath = dftdir + '/' + outdir + '/' + prefix + '.save/data-file-schema.xml'
    # verify if file exists

    # read alat and Fermi
    mytree = ET.parse(xmlpath)
    myroot = mytree.getroot()
    alat = float(myroot.find('input').find('atomic_structure').attrib['alat'])
    # factor 2 due to Hartree to Rydberg conversion
    try:
        fermi = 2 * float(myroot.find('output').find('band_structure').find('fermi_energy').text)
    except:
        fermi = 0
        print('''
###################################################
# WARNING: Fermi level not found in the XML file. #
#                                                 #
#       Using fermi = 0 instead                   #
#                                                 #
# Are you using an old version of QE?             #
###################################################
''')
    
    return alat, fermi


class read_kp_dat():
    """
    Reads the kp.dat file and builds an object with its properties:
    """
    def __init__(self, kp_path):
        """
        kp_path : path to the kp.dat file
        
        properties:
            nbnd
            nocc
            fermi
            energies
            p1, p2, p3
        """
        lines = open(kp_path, 'r').read().split('\n')
        # read nbnd and nocc from line 0
        self.nbnd = int(lines[0].split(',')[0].split('nbnd=')[1])
        # identify lines that mark labels
        line1 = where(array(lines) == '  1')[0][0]
        line2 = where(array(lines) == '  2')[0][0]
        line3 = where(array(lines) == '  3')[0][0]
        # read p1
        p1 = []
        for line in range(line1+1, line2):
            p1 += list(array(lines[line].split(), dtype='float'))
        p1 = array(p1)
        # read p2
        p2 = []
        for line in range(line2+1, line3):
            p2 += list(array(lines[line].split(), dtype='float'))
        p2 = array(p2)
        # read p3
        p3 = []
        for line in range(line3+1, len(lines)):
            p3 += list(array(lines[line].split(), dtype='float'))
        p3 = array(p3)

        # converts matrix elements into matrices
        # mix real and imag parts
        p1 = p1[0::2] + 1j*p1[1::2]
        p2 = p2[0::2] + 1j*p2[1::2]
        p3 = p3[0::2] + 1j*p3[1::2]
        # reshape into matrix and fix units
        self.p1 = p1.reshape((self.nbnd, self.nbnd)) / (20*a0)
        self.p2 = p2.reshape((self.nbnd, self.nbnd)) / (20*a0)
        self.p3 = p3.reshape((self.nbnd, self.nbnd)) / (20*a0)
