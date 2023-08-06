import numpy as np
from PToolkit import Error_function, Standaard_error_per_index
import sympy as sy
import matplotlib.pyplot as plt
import pandas as pd
import unittest
from PToolkit_test import Round_sigfig

class Test_PToolkit(unittest.TestCase):

    def test(self):
        to_round = np.array([1.52, 163, 1.7776, 1.98, 1090.897481242155221, 20.6])
        correct_round = np.array([1.5, 160.0, 1.8, 2.0, 1100.0, 21.0])
        rounded = Round_sigfig(to_round, 2)
        self.assertEqual(correct_round.tolist(), rounded.tolist())

    def test_text_rounding_normal(self):
        
        # Define array with values to round
        to_round = np.array([1.52, 163, 1.7776, 1.98, 1090.897481242155221, 20.6, 0.0012])
        
        # Round the array based on diffrent sig figs
        c1 = Round_sigfig(to_round, 1, format="text")
        c2 = Round_sigfig(to_round, 2, format="text")
        c3 = Round_sigfig(to_round, 3, format="text")
        c4 = Round_sigfig(to_round, 4, format="text")
        c5 = Round_sigfig(to_round, 5, format="text")

        # Define correct results
        ct1 = ["2", "200", "2", "2", "1000", "20", "0.001"]
        ct2 = ["1.5", "160", "1.8", "2.0", "1100", "21", "0.0012"]
        ct3 = ["1.52", "163", "1.78", "1.98", "1090", "20.6", "0.00120"]
        ct4 = ["1.520", "163.0", "1.778", "1.980", "1091", "20.60", "0.001200"]
        ct5 = ["1.5200", "163.00", "1.7776", "1.9800", "1090.9", "20.600", "0.0012000"]
        
        # Test all roundings
        self.assertEqual(ct1, c1.tolist())
        self.assertEqual(ct2, c2.tolist())
        self.assertEqual(ct3, c3.tolist())
        self.assertEqual(ct4, c4.tolist())
        self.assertEqual(ct5, c5.tolist())


    @unittest.skip("Broken")
    def test_text_rounding_up(self):
        
        # Define array with values to round
        to_round = np.array([1.52, 163, 1.7776, 1.98, 1090.897481242155221, 20.6, 0.0012])
        
        # Round the array based on diffrent sig figs
        c1 = Round_sigfig(to_round, 1, format="text", type_rounding="Up")
        c2 = Round_sigfig(to_round, 2, format="text", type_rounding="Up")
        c3 = Round_sigfig(to_round, 3, format="text", type_rounding="Up", debug=True)
        c4 = Round_sigfig(to_round, 4, format="text", type_rounding="Up")
        c5 = Round_sigfig(to_round, 5, format="text", type_rounding="Up")

        # Define correct results
        ct1 = ["2", "200", "2", "2", "2000", "30", "0.002"]
        ct2 = ["1.6", "170", "1.8", "2.0", "1100", "21", "0.0012"]
        ct3 = ["1.52", "163", "1.78", "1.98", "1090", "20.6", "0.00120"]
        ct4 = ["1.520", "163.0", "1.778", "1.980", "1091", "20.60", "0.001200"]
        ct5 = ["1.5200", "163.00", "1.7776", "1.9800", "1090.9", "20.600", "0.0012000"]
        
        # Test all roundings
        self.assertEqual(ct1, c1.tolist())
        self.assertEqual(ct2, c2.tolist())
        self.assertEqual(ct3, c3.tolist())
        self.assertEqual(ct4, c4.tolist())
        self.assertEqual(ct5, c5.tolist())
    
    @unittest.skip("Incomplete")
    def test_text_rounding_normal_small_and_big_numbers():
        to_round = np.array([1.52, 163, 1.7776, 1.98, 1090.897481242155221, 20.6, 0.0012, 0.0000000000000000000047874, 8473000000000000000000000000000000000.0])

        c1 = Round_sigfig(to_round, 1, format="text")
        c2 = Round_sigfig(to_round, 2, format="text")
        c3 = Round_sigfig(to_round, 3, format="text")
        c4 = Round_sigfig(to_round, 4, format="text")
        c5 = Round_sigfig(to_round, 5, format="text")
        ct1 = ["0.000000000000000000005", "8000000000000000000000000000000000000"]
        ct2 = ["0.0000000000000000000048", "8500000000000000000000000000000000000"]
        ct3 = ["0.00000000000000000000479""8470000000000000000000000000000000000"]
        ct4 = ["0.000000000000000000004787", "8473000000000000000000000000000000000"]
        ct5 = ["0.0000000000000000000047874", "8473000000000000000000000000000000000"]
    
    def test_Standaard_error_per_index(self):
        a1 = np.array([1.63, 2.48, 34.36, 4.847, 51.8484, 6.84749, 7.747939])
        a2 = np.array([9.4, 1000000, 5.987, 4.8474, 8.8484, 38383, 1.474747])
        a3 = np.array([1.948, 204.3, 3.9847, 4.844, 1838.7474, 0.8888888888111, 7.48474])

        correct1 = np.array([
            np.std([1.63, 9.4, 1.948], ddof=1),
            np.std([2.48, 1000000, 204.3], ddof=1),
            np.std([34.36, 5.987, 3.9847], ddof=1),
            np.std([4.847, 4.8474, 4.844], ddof=1),
            np.std([51.8484, 8.8484, 1838.7474], ddof=1),
            np.std([6.84749, 38383, 0.8888888888111], ddof=1),
            np.std([7.747939, 1.474747, 7.48474], ddof=1)
        ])/np.sqrt(3)

        correct2 = np.array([
            np.std([1.63, 9.4], ddof=1),
            np.std([2.48, 1000000], ddof=1),
            np.std([34.36, 5.987], ddof=1),
            np.std([4.847, 4.8474], ddof=1),
            np.std([51.8484, 8.8484], ddof=1),
            np.std([6.84749, 38383], ddof=1),
            np.std([7.747939, 1.474747], ddof=1)
        ])/np.sqrt(2)

        correct3 = np.array([
            np.std([1.63, 1.948], ddof=1),
            np.std([2.48, 204.3], ddof=1),
            np.std([34.36, 3.9847], ddof=1),
            np.std([4.847,  4.844], ddof=1),
            np.std([51.8484,  1838.7474], ddof=1),
            np.std([6.84749,  0.8888888888111], ddof=1),
            np.std([7.747939, 7.48474], ddof=1)
        ])/np.sqrt(2)

        A1  = Standaard_error_per_index(a1, a2, a3)
        A2 = Standaard_error_per_index(a1, a2)
        A3 = Standaard_error_per_index(a1, a3)
        

        p1 = (correct1 == A1).all()
        p2 = (correct2 == A2).all()
        p3 = (correct3 == A3).all()

        self.assertTrue(p1)
        self.assertTrue(p2)
        self.assertTrue(p3)

    @unittest.skip("Incomplete")
    def test_error_function(self):
        R_s, V_s = sy.symbols("R, V")
        I_s = V_s/R_s
        print(Error_function(I_s))

unittest.main()



