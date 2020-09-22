# coding: utf-8
# Copyright (c) Max-Planck-Institut für Eisenforschung GmbH - Computational Materials Design (CM) Department
# Distributed under the terms of "New BSD License", see the LICENSE file.

import os
import unittest
from pyiron.atomistics.structure.atoms import CrystalStructure
from pyiron_base import Project



class TestPhonopy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.file_location = os.path.dirname(os.path.abspath(__file__))
        cls.project = Project(os.path.join(cls.file_location, "test_phonopy"))
        cls.project.remove_jobs_silently(recursive=True)

    @classmethod
    def tearDownClass(cls):
        cls.file_location = os.path.dirname(os.path.abspath(__file__))
        cls.project.remove(enable=True, enforce=True)

    def test_run(self):
        job = self.project.create_job(
            'EinsteinExampleJob', "job_test"
        )
        basis = CrystalStructure(
            element="Fe", bravais_basis="bcc", lattice_constant=2.83
        )
        basis.set_initial_magnetic_moments([2,2])
        job.input['displacement_mag'] = 0
        job.input['volume_per_atom'] = basis.get_volume(per_atom=True)
        job.structure = basis
        phono = job.create_job("PhonopyJob", "phono")
        phono.run()
        structure = phono.list_structures()[0]
        magmoms = structure.get_initial_magnetic_moments()
        self.assertAlmostEqual(sum(magmoms-2), 0)


if __name__ == "__main__":
    unittest.main()
