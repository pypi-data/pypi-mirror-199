from numpy import array

# global constants
Ry = (13.6056980659) # [eV]
a0 = 0.0529177249 # [nm]
hbar = 0.658211951e-3 # [eV.ps]
m0 = (hbar**2)/(2*Ry*a0**2) # [eV.ps²/nm²] bare electron mass
h2m = Ry*a0**2 # = hbar²/2m0 [eV.nm²]
alpha = 1/137

# Pauli matrices
s0 = array([[1,0],[0,1]])
sx = array([[0,1],[1,0]])
sy = array([[0,-1j],[1j,0]])
sz = array([[1,0],[0,-1]])

# DICTIONARY KEYS TO READ THE DFT AND QSYMM DATA
# DFT   data: 0, 'x', 'y', 'z', 'xx', 'xy', ...
# QSYMM data: 1, 'k_x', 'k_y', 'k_z', 'k_x**2', 'kx*k_z', ...
#                 kx**2 = kx*kx (sympy simplifies it)

strKs = ['k_x', 'k_y', 'k_z']
QSkeys = []
QSkeys += [1] # order 0
QSkeys += strKs # order 1
QSkeys += [strKs[i]+'*'+strKs[j] for i in range(3) for j in range(i,3)] # order 2
QSkeys += [strKs[i]+'*'+strKs[j]+'*'+strKs[l] for i in range(3) for j in range(i,3) for l in range(j,3)] # order 3

strKs = ['x', 'y', 'z']
DFTkeys = []
DFTkeys += [0]
DFTkeys += strKs
DFTkeys += [strKs[i]+strKs[j] for i in range(3) for j in range(i,3)]
DFTkeys += [strKs[i]+strKs[j]+strKs[l] for i in range(3) for j in range(i,3) for l in range(j,3)]