import unittest
import opf
from pathlib import Path
import pyomo.environ as pyo
import math
import time


class DCOPFPTDFSolveTest(unittest.TestCase):
    def test_solve_case5(self):
        pglibpath = Path("/storage/home/hcoda1/7/spark719/RAMC/pglib-opf")
        # matpower_fn = Path("./data/pglib_opf_case5_pjm.m")
        # matpower_fn = Path("/storage/home/hcoda1/7/spark719/RAMC/pglib-opf/pglib_opf_case10480_goc.m")
        # matpower_fn = Path("/storage/home/hcoda1/7/spark719/RAMC/pglib-opf/pglib_opf_case3022_goc.m")
        # matpower_fn = Path("/storage/home/hcoda1/7/spark719/RAMC/pglib-opf/pglib_opf_case1354_pegase.m")
        # matpower_fn = Path("/storage/home/hcoda1/7/spark719/RAMC/pglib-opf/pglib_opf_case89_pegase.m") # for DCOPF and PTDF, it is slightly different
        filename = "pglib_opf_case5_pjm.m"
        # filename = "pglib_opf_case200_activ.m" # for DCOPF-PTDF, it is infeasible
        # filename = "pglib_opf_case3022_goc.m"
        # filename = "pglib_opf_case1354_pegase.m"
        # filename = "pglib_opf_case10480_goc.m"
        # filename = 'pglib_opf_case6515_rte.m'
        # filename = 'pglib_opf_case2868_rte.m'
        # filename = 'pglib_opf_case30000_goc.m'

        matpower_fn = pglibpath/filename # for DCOPF-PTDF, it is infeasible
        network = opf.parse_file(matpower_fn)
        
        solver = pyo.SolverFactory("ipopt")
        # solver = pyo.SolverFactory("gurobi")

        model = opf.build_model('acopf')
        t0 = time.time()
        model.instantiate(network, verbose=True)
        print('instantiate_', time.time()-t0)
        results = model.solve(solver_option={'linear_solver': 'ma27'}, tee=True)


        # model = opf.build_model('dcopf')
        # instance = model.instantiate_model(network, verbose=True)
        # results = solver.solve(instance, options={'linear_solver': 'ma27'}, tee=True)



