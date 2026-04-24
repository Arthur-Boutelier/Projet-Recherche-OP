from ProblemeTransport import *
from function import *
Pb = ProblemeTransport("test.txt")
#Pb.hammer(verbose=True)
Pb.nord_west()
mat = [[1,0,0],[0,0,1],[1,1,0]]
print(Pb.calcul_cout_tot())
print(Pb.prob_transp)
Pb.calcul_cout_potentiel()
Pb.calcul_cout_marginaux()
#print(est_connexe(mat))