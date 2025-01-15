import unittest
import os
import pydicom

from scripts.parse_dicom import get_structure_names, get_max_dose

class TestParseDicom(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        cls.dicom_dir = os.path.join(script_dir, "..", "data", "dicom", "datasets_dicom")
        cls.rtstruct_file = None
        cls.rtdose_file = None

        for root, _, files in os.walk(cls.dicom_dir):
            for file in files:
                if file.lower().endswith(".dcm"):
                    path = os.path.join(root, file)
                    try:
                        ds = pydicom.dcmread(path, stop_before_pixels=True)
                        modality = ds.Modality
                        if modality == "RTSTRUCT" and cls.rtstruct_file is None:
                            cls.rtstruct_file = path
                        elif modality == "RTDOSE" and cls.rtdose_file is None:
                            cls.rtdose_file = path
                    except:
                        continue
                if cls.rtstruct_file and cls.rtdose_file:
                    break
            if cls.rtstruct_file and cls.rtdose_file:
                break

    def test_get_structure_names(self):
        if not self.rtstruct_file:
            self.skipTest("No se encontró ningún RTSTRUCT en data/dicom/datasets_dicom para test.")
        estructuras = get_structure_names(self.rtstruct_file)
        self.assertTrue(len(estructuras) > 0)

    def test_get_max_dose(self):
        if not self.rtdose_file:
            self.skipTest("No se encontró ningún RTDOSE en data/dicom/datasets_dicom para test.")
        max_dose = get_max_dose(self.rtdose_file)
        self.assertGreater(max_dose, 0)

if __name__ == '__main__':
    unittest.main()
