from ProblemeTransport import *
from function import *
import time
"""
Pb = ProblemeTransport("test.txt")
#Pb.hammer(verbose=True)
Pb.nord_west()
mat = [[1,0,0],[0,0,1],[1,1,0]]
print(Pb.calcul_cout_tot())
print(Pb.prob_transp)
Pb.calcul_cout_potentiel()
Pb.calcul_cout_marginaux()
print(Pb.est_connexe())"""

temp_init = time.perf_counter()
Pb = ProblemeTransport.create_random_pb(10000, 10000)
print(f"Creation : {-temp_init + time.perf_counter()}")
temp_init = time.perf_counter()
Pb.nord_west()
print(f"Nord West : {-temp_init + time.perf_counter()}")
temp_init = time.perf_counter()
Pb.hammer(verbose=False)
print(f"Hammer : {-temp_init + time.perf_counter()}")