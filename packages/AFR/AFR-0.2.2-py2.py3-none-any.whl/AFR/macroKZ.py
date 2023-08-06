import pandas as pd

def load_macroKZ():
    """
           Loads finratKZ dataset. More details in the description of the dataset.

           """

    file_path = pkg_resources.resource_filename ( 'AFR', 'load/macroKZ.csv' )
    df = pd.read_csv ( file_path )
    return df