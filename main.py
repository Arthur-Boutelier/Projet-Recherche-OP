from ProblemeTransport import *
from function import *
Pb = ProblemeTransport("test.txt")
#Pb.hammer(verbose=True)
Pb.nord_west()
mat = [[1,0,0],[0,0,1],[1,1,0]]
print(Pb.calcul_cout_tot())
print(Pb.prob_transp)
print(est_connexe(mat))