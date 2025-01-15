import os
from dicompylercore import dicomparser
from parse_dicom import get_structure_names, get_max_dose

def process_dicom_files(base_path):
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.lower().endswith('.dcm'):
                file_path = os.path.join(root, file)
                
                try:
                    dp = dicomparser.DicomParser(file_path)
                    ds = dp.ds
                    modality = ds.get("Modality", "Desconocido")
                    
                    print(f"Archivo: {file_path}")
                    print(f"  Modality: {modality}")

                    if modality == "RTSTRUCT":
                        estructuras = get_structure_names(file_path)
                        print("  Estructuras encontradas:")
                        for estructura in estructuras:
                            print(f"    - {estructura}")

                    elif modality == "RTDOSE":
                        max_d = get_max_dose(file_path)
                        print(f"  Dosis máxima: {max_d} Gy (aprox.)")

                    print("-" * 40)
                
                except Exception as e:
                    print(f"No se pudo leer {file_path}: {e}")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dicom_dir = os.path.join(script_dir, "..", "data", "dicom", "datasets_dicom")
    process_dicom_files(dicom_dir)

if __name__ == "__main__":
    main()
