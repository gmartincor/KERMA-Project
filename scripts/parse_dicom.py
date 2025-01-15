from dicompylercore import dicomparser

def get_structure_names(rtstruct_path):
    """
    Dado un archivo DICOM RTSTRUCT, obtiene la lista de nombres de estructuras
    utilizando dicompyler-core.
    """
    dp = dicomparser.DicomParser(rtstruct_path)
    ds = dp.ds
    if ds.Modality != "RTSTRUCT":
        raise ValueError(f"El archivo {rtstruct_path} no es de tipo RTSTRUCT.")
    structures = dp.GetStructures()
    structure_names = []
    for struct_id in structures:
        struct_info = structures[struct_id]
        structure_names.append(struct_info["name"])
    return structure_names

def get_max_dose(rtdose_path):
    """
    Dado un archivo DICOM RTDOSE, obtiene la dosis máxima (en Gy aproximados)
    usando dicompyler-core (similar a pydicom pero con dicomparser).
    """
    dp = dicomparser.DicomParser(rtdose_path)
    ds = dp.ds
    if ds.Modality != "RTDOSE":
        raise ValueError(f"El archivo {rtdose_path} no es de tipo RTDOSE.")
    dose_array = ds.pixel_array.astype(float)
    dose_grid_scaling = getattr(ds, "DoseGridScaling", 1.0)
    dose_array *= dose_grid_scaling
    max_dose = float(dose_array.max())
    return max_dose
