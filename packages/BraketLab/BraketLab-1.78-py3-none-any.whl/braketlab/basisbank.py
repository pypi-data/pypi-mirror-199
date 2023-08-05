import sympy as sp
import numpy as np

import braketlab.solid_harmonics as sh
import braketlab.real_solid_harmonics as rsh
import braketlab.hydrogen as hy
import braketlab.harmonic_oscillator as ho

from braketlab.core import ket, get_ordered_symbols, get_default_variables

def extract_pyscf_basis(mol):
    """
    Get a braketlab basis from a pyscf mol object

    ## Arguments 

    |mol | pySCF molecule object |

    ## Returns

    A list containing braketlab basis functions


    ## Example usage

    ```python
    from pyscf import gto
    mol = gto.Mole()
    mol.build(atom = '''O 0 0 0; H  0 1 0; H 0 0 1''',basis = 'pvdz')
    basis = extract_pyscf_basis(mol)
    ```

    """
    
    # get contraction coefficients from pyscf
    pmol, ctr_coeff = mol.to_uncontracted_cartesian_basis()
    
    # get the uncontracted overlap matrix
    overlap_uncontracted = pmol.intor('int1e_ovlp')
    
    contracted_aos = []
    c_count = 0 # counter for selecting blocks in overlap_uncontracted
    
    for contr in range(mol.nbas):
        l = mol.bas_angular(contr)  #angular momentum of contracted
        contr_coeff = np.array(mol.bas_ctr_coeff(contr)) #contraction coefficients
        exponent = mol.bas_exp(contr).ravel() #exponents of contraction
        
        # overlap for current contracted
        s_c = overlap_uncontracted[c_count:c_count+len(exponent)*(2*l + 1),c_count:c_count+len(exponent)*(2*l+1)]
        
        le, l1 = len(exponent), 2*l +1

        
        si = np.arange(le*l1).reshape(le, l1).T.ravel()
        s_c = s_c[si, :][:, si]
        
        ci = 0
        
        for m in range(-l, l+1):
            norm = s_c[ci:ci+2*l+1, ci:ci+2*l+1]
            
            for cc in range(contr_coeff.shape[1]):
                cco = contr_coeff[:, cc]
                N = np.sum( (cco[:,None]*cco[None, :])*s_c[ci:ci+2*l+1, ci:ci+2*l+1] )**-.5

                p = cco[0]*get_gto(exponent[0], l, m, position = np.array(mol.bas_coord(contr)))
                for b in range(1, len(contr_coeff)):
                    p += cco[b]*get_gto(exponent[b], l, m, position = np.array(mol.bas_coord(contr)))
                contracted_aos.append(p)
            ci += len(contr_coeff)
            
        c_count += le*l1

    return contracted_aos

def get_default_variables(p, n = 3):
    variables = []
    for i in range(n):
        variables.append(sp.Symbol("x_{%i; %i}" % (p, i)))
    return variables



def get_hydrogen_function(n,l,m, position = np.array([0,0,0])):
    """
    Returns a ket containing the hydrogen eigenfunction with quantum numbers n,l,m
    located at position
    """
    psi = hy.hydrogen_function(n,l,m)
    #vars = list(psi.free_symbols)
    vars = get_ordered_symbols(psi)
    symbols = get_default_variables(0, len(vars))
    for i in range(len(vars)):
        psi = psi.subs(vars[i], symbols[i])

    



    return ket(psi, name = "%i,%i,%i" % (n,l,m), position = position)

def get_harmonic_oscillator_function(n, omega = 1, position = 0):
    """
    Returns a ket containing the harmonic oscillator energy eigenfunction with quantum number n
    located at position
    """
    psi = ho.psi_ho(n)
    symbols = np.array(list(psi.free_symbols))
    l_symbols = np.argsort([i.name for i in symbols])
    symbols = symbols[l_symbols]
    #vars = list(psi.free_symbols)
    vars = get_default_variables(0, len(symbols))
    for i in range(len(vars)):
        psi = psi.subs(symbols[i], vars[i])

    return ket(psi, name = "%i" % n, energy = [omega*(.5+n)], position = np.array([position]))

def get_gto(a,l,m, position = np.array([0,0,0])):
    """
    Returns a ket containing the gaussian type primitive orbital with exponent a, 
    and solid harmonic gaussian angular part defined by l and m
    located at position
    """
    psi = rsh.get_gto(a,l,m)

    

    symbols = np.array(list(psi.free_symbols))
    l_symbols = np.argsort([i.name for i in symbols])
    symbols = symbols[l_symbols]
    #vars = list(psi.free_symbols)
    vars = get_default_variables(0, len(symbols))
    for i in range(len(vars)):
        psi = psi.subs(symbols[i], vars[i])
    


    return ket(psi, name = "\chi_{%i,%i}^{%.2f}" % (l,m,a), position = position)

def get_sto(a,w,n,l,m, position = np.array([0,0,0])):
    """
    Returns a ket containing the slater type orbital with exponent a, 
    weight w,
    and solid harmonic gaussian angular part defined by l and m
    located at position
    """
    psi = sh.get_sto(a,w,n,l,m)

    symbols = np.array(list(psi.free_symbols))
    l_symbols = np.argsort([i.name for i in symbols])
    symbols = symbols[l_symbols]
    #vars = list(psi.free_symbols)
    vars = get_default_variables(0, len(symbols))
    for i in range(len(vars)):
        psi = psi.subs(symbols[i], vars[i])

    #vars = list(psi.free_symbols)
    #symbols = bk.get_default_variables(0, len(vars))
    #for i in range(len(vars)):
    #    psi = psi.subs(vars[i], symbols[i])
    return ket(psi, name  = "\chi_{%i,%i}^{%.2f}" % (l,m,a), position = position)

