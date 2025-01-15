import os
import numpy as np
from django.shortcuts import render
from scripts.parse_dicom import get_structure_names, get_max_dose
from scripts.parse_dynalog_pylinac import accumulate_fluence

def home(request):
    return render(request, 'kerma_app/index.html')

def show_dicom_results(request):
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    dicom_dir = os.path.join(base_dir, "data", "dicom", "datasets_dicom")

    rtstruct_list = []
    rtdose_list = []

    from dicompylercore import dicomparser

    for root, dirs, files in os.walk(dicom_dir):
        for f in files:
            if f.lower().endswith('.dcm'):
                path = os.path.join(root, f)
                try:
                    dp = dicomparser.DicomParser(path)
                    ds = dp.ds
                    modality = ds.Modality

                    if modality == "RTSTRUCT":
                        names = get_structure_names(path)
                        rtstruct_list.append({
                            "file": path,
                            "structures": names
                        })

                    elif modality == "RTDOSE":
                        dose = get_max_dose(path)
                        rtdose_list.append({
                            "file": path,
                            "max_dose": dose
                        })
                except:
                    continue

    context = {
        'rtstruct_list': rtstruct_list,
        'rtdose_list': rtdose_list,
    }
    return render(request, 'kerma_app/dicom_results.html', context)

def show_dynalog_results(request):
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    dynalog_dir = os.path.join(base_dir, "data", "dynalogs", "datasets_dynalogs")

    fileA = None
    fileB = None
    for root, dirs, files in os.walk(dynalog_dir):
        for f in files:
            if f.lower().endswith('.dlg'):
                if 'A' in f and fileA is None:
                    fileA = os.path.join(root, f)
                elif 'B' in f and fileB is None:
                    fileB = os.path.join(root, f)
        if fileA and fileB:
            break

    fluence_actual = None
    fluence_expected = None

    if fileA and fileB:
        from scripts.parse_dynalog_pylinac import accumulate_fluence
        fluence_actual, fluence_expected = accumulate_fluence([fileA, fileB])

    dims = None
    sum_actual = None
    sum_expected = None
    error_total = None
    mean_actual = None
    mean_expected = None
    mean_error = None
    mean_abs_error = None
    error_percentage = None

    if (fluence_actual is not None) and (fluence_expected is not None):
        dims = fluence_actual.shape
        sum_actual = float(np.sum(fluence_actual))
        sum_expected = float(np.sum(fluence_expected))
        error_total = sum_actual - sum_expected
        mean_actual = float(fluence_actual.mean())
        mean_expected = float(fluence_expected.mean())
        mean_error = float((fluence_actual - fluence_expected).mean())
        mean_abs_error = float(np.abs(fluence_actual - fluence_expected).mean())

        if sum_expected != 0:
            error_percentage = (error_total / sum_expected) * 100
        else:
            error_percentage = float('nan')

    context = {
        'fileA': fileA,
        'fileB': fileB,
        'dims': dims,
        'sum_actual': sum_actual,
        'sum_expected': sum_expected,
        'error_total': error_total,
        'mean_actual': mean_actual,
        'mean_expected': mean_expected,
        'mean_error': mean_error,
        'mean_abs_error': mean_abs_error,
        'error_percentage': error_percentage,
    }
    return render(request, 'kerma_app/dynalog_results.html', context)
