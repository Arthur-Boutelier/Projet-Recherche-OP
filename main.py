from ProblemeTransport import *
from function import *
import time
import Benchmark
"""
Pb = ProblemeTransport.charger_fichier("test.txt")
Pb1 = ProblemeTransport.charger_fichier("test.txt")
#Pb.hammer(verbose=True)
Pb.nord_west()
Pb.marche_pied_potentiel()
Pb1.hammer()
print(Pb.prob_transp)
print(Pb1.prob_transp)
est_connexe, x = Pb1.est_connexe()
Pb1.rendre_connexe(x)
print(Pb1.prob_transp)
temp_init = time.perf_counter()
Pb = ProblemeTransport.create_random_pb(10000, 10000)
print(f"Creation : {-temp_init + time.perf_counter()}")
temp_init = time.perf_counter()
Pb.hammer(verbose=False)
print(f"Nord West : {-temp_init + time.perf_counter()}")
temp_init = time.perf_counter()
Pb.marche_pied_potentiel(verbose=False, partial=True)
print(f"Hammer : {-temp_init + time.perf_counter()}")
"""
Benchmark.lancer_benchmark()