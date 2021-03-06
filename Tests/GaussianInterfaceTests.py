
from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.GaussianInterface import *
import sys, os, numpy as np

class GaussianInterfaceTests(TestCase):

    test_log_water = TestManager.test_data("water_OH_scan.log")
    test_log_freq = TestManager.test_data("water_freq.log")
    test_log_opt = TestManager.test_data("water_dimer_test.log")
    test_fchk = TestManager.test_data("water_freq.fchk")
    test_log_h2 = TestManager.test_data("outer_H2_scan_new.log")
    test_log_tet = TestManager.test_data("2Dtet_rigid_in.log")
    test_log_tet_rel = TestManager.test_data("2Dtet_relax_in.log")

    @debugTest
    def test_GetLogInfo(self):
        with GaussianLogReader(TestManager.test_data("tbhp_030.log")) as reader:
            parse = reader.parse("Header")
        self.assertIn("P", parse["Header"].job)

    @debugTest
    def test_DefaultLogParse(self):
        with GaussianLogReader(TestManager.test_data("tbhp_030.log")) as reader:
            parse = reader.parse()
        self.assertLess(parse["OptimizedScanEnergies"][1][0], -308)

    @validationTest
    def test_GetDipoles(self):
        with GaussianLogReader(self.test_log_water) as reader:
            parse = reader.parse("DipoleMoments")
        dips = parse["DipoleMoments"]
        self.assertIsInstance(dips, np.ndarray)
        self.assertEquals(dips.shape, (251, 3))

    @validationTest
    def test_GaussianLoad(self):
        with GaussianLogReader(self.test_log_water) as reader:
            parse = reader.parse("InputZMatrix")
        zmat = parse["InputZMatrix"]
        self.assertIsInstance(zmat, str)

    @validationTest
    def test_GaussianAllCartesians(self):
        with GaussianLogReader(self.test_log_water) as reader:
            parse = reader.parse("CartesianCoordinates")
        carts = parse["CartesianCoordinates"]
        self.assertIsInstance(carts[1], np.ndarray)
        self.assertEquals(carts[1].shape, (502, 3, 3))

    @validationTest
    def test_GaussianCartesians(self):
        with GaussianLogReader(self.test_log_water) as reader:
            parse = reader.parse("CartesianCoordinates", num=15)
        carts = parse["CartesianCoordinates"]
        self.assertIsInstance(carts[1], np.ndarray)
        self.assertEquals(carts[1].shape, (15, 3, 3))

    @validationTest
    def test_GaussianStandardCartesians(self):
        with GaussianLogReader(self.test_log_water) as reader:
            parse = reader.parse("StandardCartesianCoordinates", num=15)
        carts = parse["StandardCartesianCoordinates"]
        self.assertIsInstance(carts[1], np.ndarray)
        self.assertEquals(carts[1].shape, (15, 3, 3))

    @validationTest
    def test_GaussianZMatrixCartesians(self):
        with GaussianLogReader(self.test_log_water) as reader:
            parse = reader.parse("ZMatCartesianCoordinates", num=15)
        carts = parse["ZMatCartesianCoordinates"]
        self.assertIsInstance(carts[1], np.ndarray)
        self.assertEquals(carts[1].shape, (15, 3, 3))

    @validationTest
    def test_GZMatCoords(self):
        with GaussianLogReader(self.test_log_water) as reader:
            parse = reader.parse("ZMatrices", num = 3)
        zmats = parse["ZMatrices"]
        # print(zmats, file=sys.stderr)
        self.assertIsInstance(zmats[0][1][0], str)
        self.assertIsInstance(zmats[1], np.ndarray)
        self.assertEquals(zmats[1].shape, (3, 3))
        self.assertEquals(zmats[2].shape, (3, 3, 3))

    @validationTest
    def test_ScanEnergies(self):
        with GaussianLogReader(self.test_log_tet) as reader:
            parse = reader.parse("ScanEnergies", num=3)
        engs = parse["ScanEnergies"]
        self.assertIsInstance(engs, dict)
        self.assertIsInstance(engs["values"], np.ndarray)
        self.assertIsInstance(engs["coords"], np.ndarray)
        self.assertEquals(engs["coords"].shape, (5,))
        self.assertEquals(engs["values"].shape, (30, 5))

    @validationTest
    def test_GZMatCoordsBiggie(self):
        num_pulled = 5
        num_entries = 8
        with GaussianLogReader(self.test_log_h2) as reader:
            parse = reader.parse("ZMatrices", num = num_pulled)
        zmats = parse["ZMatrices"]
        # print(zmats, file=sys.stderr)
        self.assertIsInstance(zmats[1], np.ndarray)
        self.assertEquals(zmats[1].shape, (num_entries, 3))
        self.assertEquals(zmats[2].shape, (num_pulled, num_entries, 3))

    @validationTest
    def test_OptScanEnergies(self):
        with GaussianLogReader(self.test_log_opt) as reader:
            parse = reader.parse("OptimizedScanEnergies")
        e, c = parse["OptimizedScanEnergies"]
        self.assertIsInstance(e, np.ndarray)
        self.assertEquals(e.shape, (10,))
        self.assertEquals(len(c.keys()), 14)
        self.assertEquals(list(c.values())[0].shape, (10,))

    @debugTest
    def test_OptDips(self):
        with GaussianLogReader(self.test_log_tet_rel) as reader:
            parse = reader.parse(["OptimizedScanEnergies", "OptimizedDipoleMoments"])
        c = np.array(parse["OptimizedDipoleMoments"])
        self.assertIsInstance(c, np.ndarray)
        self.assertEquals(c.shape, (30,3))

    @validationTest
    def test_XMatrix(self):
        file=TestManager.test_data('qooh1.log')
        with GaussianLogReader(file) as reader:
            parse = reader.parse("XMatrix")
        X = np.array(parse["XMatrix"])

        self.assertIsInstance(X, np.ndarray)
        self.assertEquals(X.shape, (39, 39))
        self.assertEquals(X[0, 10], -0.126703)
        self.assertEquals(X[33, 26], -0.642702E-1)

    @validationTest
    def test_Fchk(self):
        with GaussianFChkReader(self.test_fchk) as reader:
            parse = reader.parse()
        key = next(iter(parse.keys()))
        self.assertIsInstance(key, str)

    @validationTest
    def test_ForceConstants(self):
        n = 3 # water
        with GaussianFChkReader(self.test_fchk) as reader:
            parse = reader.parse("ForceConstants")
        fcs = parse["ForceConstants"]
        self.assertEquals(fcs.n, n)
        self.assertEquals(fcs.array.shape, (3*n, 3*n))

    @validationTest
    def test_ForceThirdDerivatives(self):
        n = 3 # water
        with GaussianFChkReader(self.test_fchk) as reader:
            parse = reader.parse("ForceDerivatives")
        fcs = parse["ForceDerivatives"]
        tds = fcs.third_deriv_array
        self.assertEquals(fcs.n, n)
        self.assertEquals(tds.shape, ((3*n-6), (3*n), 3*n))
        a = tds[0]
        self.assertTrue(
            np.allclose(tds[0], tds[0].T, rtol=1e-08, atol=1e-08)
        )
        self.assertTrue(
            np.allclose(tds[1], tds[1].T, rtol=1e-08, atol=1e-08)
        )
        self.assertTrue(
            np.allclose(tds[2], tds[2].T, rtol=1e-08, atol=1e-08)
        )

    @validationTest
    def test_ForceFourthDerivatives(self):
        n = 3 # water
        with GaussianFChkReader(self.test_fchk) as reader:
            parse = reader.parse("ForceDerivatives")
        fcs = parse["ForceDerivatives"]
        tds = fcs.fourth_deriv_array
        self.assertEquals(fcs.n, n)
        self.assertEquals(tds.shape, ((3*n-6), (3*n-6), (3*n), 3*n)) # it's a SparseTensor now
        slice_0 = tds[0, 0].toarray()
        slice_1 = tds[1, 1].toarray()
        slice_2 = tds[2, 2].toarray()
        self.assertTrue(
            np.allclose(slice_0, slice_0.T, rtol=1e-08, atol=1e-08)
        )
        self.assertTrue(
            np.allclose(slice_1, slice_1.T, rtol=1e-08, atol=1e-08)
        )
        self.assertTrue(
            np.allclose(slice_2, slice_2.T, rtol=1e-08, atol=1e-08)
        )

    @validationTest
    def test_FchkMasses(self):
        n = 3 # water
        with GaussianFChkReader(self.test_fchk) as reader:
            parse = reader.parse("AtomicMasses")
        masses = parse["AtomicMasses"]
        self.assertEquals(len(masses), n)

    @validationTest
    def test_GaussianJobWriter(self):
        job = GaussianJob(
            "water scan",
            description="Simple water scan",
            config= GaussianJob.Config(
                NProc = 4,
                Mem = '1000MB'
            ),
            job= GaussianJob.Job(
                'Scan'
            ),
            system = GaussianJob.System(
                charge=0,
                molecule=[
                    ["O", "H", "H"],
                    [
                        [0, 0, 0],
                        [.987, 0, 0],
                        [0, .987, 0]
                    ]
                ],
                vars=[
                    GaussianJob.System.Variable("y1", 0., 10., .1),
                    GaussianJob.System.Constant("x1", 10)
                ]

            )
        )
        # print(job.write(), file=sys.stderr)
        self.assertIsInstance(job.format(), str)
