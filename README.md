# KERMA Project

KERMA is a Django-based web application designed for analyzing radiation therapy data, specifically focused on processing DICOM files and Dynalog machine log files. The application provides a user-friendly interface to visualize and analyze radiation treatment planning and delivery data.

## Overview

The KERMA Project provides tools for:

- **DICOM Analysis**: Processing RTSTRUCT and RTDOSE files to extract radiation therapy structure information and dose distributions
- **Dynalog Analysis**: Analyzing machine log files to compare actual vs. planned radiation delivery through fluence map calculations
- **Web Interface**: A Django-powered web application for easy data visualization and analysis
- **Statistical Analysis**: Comprehensive error analysis and quality assurance metrics for radiation therapy delivery

## Features

### DICOM Processing
- Extract structure names from RTSTRUCT files
- Calculate maximum dose values from RTDOSE files
- Support for standard DICOM RT objects used in radiation therapy

### Dynalog Analysis
- Process Varian dynalog files (.dlg format)
- Calculate actual vs. expected fluence maps
- Statistical analysis including:
  - Total fluence comparison
  - Mean fluence values
  - Error calculations (absolute and percentage)
  - Quality assurance metrics

### Web Interface
- Clean, responsive web interface
- Dark/light theme support
- Real-time data visualization
- Navigation between different analysis sections

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Required Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install django numpy pydicom dicompylercore pylinac
```

### Full Installation

1. Clone the repository:
```bash
git clone https://github.com/gmartincor/KERMA-Project.git
cd KERMA-Project
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up the Django application:
```bash
cd kerma_site
python manage.py migrate
```

4. Run the development server:
```bash
python manage.py runserver
```

5. Access the application at `http://localhost:8000`

## Usage

### Web Application

1. **Home Page**: Navigate to the main page to access different analysis sections
2. **DICOM Results**: View processed DICOM files showing:
   - RTSTRUCT files with extracted structure names
   - RTDOSE files with maximum dose values
3. **Dynalog Results**: View dynalog analysis showing:
   - Processed dynalog file pairs (A and B files)
   - Fluence calculations and statistical analysis
   - Error metrics and quality assurance data

### Command Line Scripts

#### DICOM Inspection
```bash
cd scripts
python inspection_dicom.py
```

#### Dynalog Processing
```bash
cd scripts
python parse_dynalog_pylinac.py
```

## Project Structure

```
KERMA-Project/
├── data/                          # Data directory
│   ├── dicom/datasets_dicom/      # DICOM files storage
│   └── dynalogs/datasets_dynalogs/ # Dynalog files storage
├── kerma_site/                    # Django web application
│   ├── kerma_app/                 # Main Django app
│   │   ├── static/                # CSS, JS, and static files
│   │   ├── templates/             # HTML templates
│   │   ├── views.py               # Django views
│   │   ├── urls.py                # URL routing
│   │   └── tests.py               # Django tests
│   ├── kerma_site/                # Django project settings
│   └── manage.py                  # Django management script
├── scripts/                       # Analysis scripts
│   ├── parse_dicom.py            # DICOM processing functions
│   ├── parse_dynalog_pylinac.py  # Dynalog processing functions
│   └── inspection_dicom.py       # DICOM inspection utility
├── tests/                         # Unit tests
│   ├── test_dicom.py             # DICOM processing tests
│   └── test_dynalog.py           # Dynalog processing tests
├── requirements.txt               # Python dependencies
├── .gitignore                     # Git ignore file
└── README.md                      # Project documentation
```

## Data Formats

### DICOM Files
- **RTSTRUCT**: Radiation therapy structure files containing organ and target contours
- **RTDOSE**: Radiation therapy dose distribution files

### Dynalog Files
- **.dlg files**: Varian linear accelerator log files
- **File pairs**: Requires both A and B files for complete analysis
- **Format**: Binary files containing machine delivery data

## Development

### Setting up Development Environment

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install development dependencies:
```bash
pip install -r requirements.txt
```

3. Run tests:
```bash
# Run Django tests
cd kerma_site
python manage.py test

# Run unit tests
cd ..
python -m unittest discover tests/
```

### Key Components

#### Django Views (`kerma_site/kerma_app/views.py`)
- `home()`: Main page view
- `show_dicom_results()`: Processes and displays DICOM analysis
- `show_dynalog_results()`: Processes and displays dynalog analysis

#### Analysis Scripts
- `parse_dicom.py`: Core DICOM processing functions
  - `get_structure_names()`: Extract structure names from RTSTRUCT
  - `get_max_dose()`: Calculate maximum dose from RTDOSE
- `parse_dynalog_pylinac.py`: Core dynalog processing functions
  - `accumulate_fluence()`: Process dynalog files and calculate fluence maps

### Testing

The project includes comprehensive unit tests:

```bash
# Run specific test modules
python -m unittest tests.test_dicom
python -m unittest tests.test_dynalog

# Run all tests
python -m unittest discover tests/
```

## Dependencies

### Core Dependencies
- **Django**: Web framework for the user interface
- **NumPy**: Numerical computing for data analysis
- **pydicom**: DICOM file reading and processing
- **dicompylercore**: Advanced DICOM RT analysis
- **pylinac**: Medical linear accelerator analysis

### Development Dependencies
- **unittest**: Python's built-in testing framework

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Add tests for new functionality
5. Run the test suite to ensure everything works
6. Commit your changes (`git commit -am 'Add some feature'`)
7. Push to the branch (`git push origin feature/your-feature`)
8. Create a Pull Request

## License

This project is open source. Please check the repository for license details.

## Medical Disclaimer

This software is intended for research and educational purposes. It should not be used for clinical decision-making without proper validation and regulatory approval. Always consult with qualified medical physicists and follow institutional protocols for radiation therapy quality assurance.

## Support

For questions, issues, or contributions, please use the GitHub issues tracker or contact the project maintainers.