import os
import numpy as np
from pylinac import load_log

def accumulate_fluence(log_paths):
    fluence_actual_acc = None
    fluence_expected_acc = None

    for path in log_paths:
        log = load_log(path)
        actual_map = log.fluence.actual.calc_map()
        expected_map = log.fluence.expected.calc_map()

        if fluence_actual_acc is None:
            fluence_actual_acc = actual_map.copy()
            fluence_expected_acc = expected_map.copy()
        else:
            fluence_actual_acc += actual_map
            fluence_expected_acc += expected_map

    return fluence_actual_acc, fluence_expected_acc

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    logs_dir = os.path.join(script_dir, "..", "data", "dynalogs", "datasets_dynalogs")
    
    log_a = "A20230215192350_2100EX20.dlg"
    log_b = "B20230215192350_2100EX20.dlg"
    
    log_a_path = os.path.join(logs_dir, log_a)
    log_b_path = os.path.join(logs_dir, log_b)
    
    log_paths = [log_a_path, log_b_path]
    
    fluence_actual, fluence_expected = accumulate_fluence(log_paths)
    
    if fluence_actual is None or fluence_expected is None:
        print("Could not accumulate fluence (empty or invalid files?).")
        return
    
    fluence_error = fluence_actual - fluence_expected
    
    actual_total = float(fluence_actual.sum())
    expected_total = float(fluence_expected.sum())
    error_total = float(fluence_error.sum())

    print("=== FLUENCE RESULTS (multiple files) ===")
    print(f"Dimensions of accumulated fluence: {fluence_actual.shape}")
    print(f"ACTUAL Fluence  - Total sum: {actual_total:.3f}")
    print(f"EXPECTED Fluence  - Total sum: {expected_total:.3f}")
    print(f"Error (total)  - Total sum: {error_total:.3f}")
    
    actual_mean = float(fluence_actual.mean())
    expected_mean = float(fluence_expected.mean())
    error_mean = float(fluence_error.mean())
    print(f"ACTUAL Fluence  - Mean: {actual_mean:.3f}")
    print(f"EXPECTED Fluence  - Mean: {expected_mean:.3f}")
    print(f"Error (mean)  - Mean: {error_mean:.3f}")
    
    error_abs_mean = float(np.abs(fluence_error).mean())
    print(f"Mean absolute error: {error_abs_mean:.3f}")
    
    if expected_total != 0:
        error_percentage = (error_total / expected_total) * 100
    else:
        error_percentage = float('nan')
    print(f"Global percentage error relative to plan: {error_percentage:.2f} %")

if __name__ == "__main__":
    main()
