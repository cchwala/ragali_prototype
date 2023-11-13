import pandas as pd
import re


def get_cml_metadata_convention():
    df = pd.read_csv(
        'https://raw.githubusercontent.com/OpenSenseAction/OS_data_format_conventions/main/netCDF_CML.adoc',
        sep='|',
        skiprows=9,
    )

    df = df.drop(columns='Unnamed: 0').drop(0).set_index('Unnamed: 1')
    df.index.name = 'Dimensions'

    return df


def check_required_cml_metadata(ds):
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    df = get_cml_metadata_convention()
    df_required = df[(df.Requisite == ' Required') | (df.Requisite == ' Required*')]

    print('Checking required variables...')
    error_count = 0
    for row in df_required.iterrows():
        split = re.split(r'\(|\)', row[0])
        var_name, dims = split[0].strip(), tuple(split[1].split(','))
        print(f' {var_name}')
        try:
            ds[var_name]
            if ds[var_name].dims != dims:
                print(f"  {FAIL}dims of variable '{var_name}' are {ds[var_name].dims} but have to be {dims}{ENDC}")
                error_count += 1
            else:
                print(f"  {OKGREEN}OK{ENDC}")
        except:
            print(f"  {FAIL}Required variable '{var_name}' is missing{ENDC}")
            error_count += 1

    print()
    print(f"{FAIL}{error_count} errors found{ENDC}")
