==========================
Experiment Script Overview
==========================

This folder contains the several scripts, each one acting as a pycomex Experiment module.
Each script is executable and will execute an experiment with a specific purpose. These experiments will
create artifacts, which will automatically be stored within their own archive folder within the nested
``results`` folder. For more information...

The following list aims to provide a brief overview over the purpose of each of the scripts.

* ``generate_molecule_dataset_from_csv.py``: Base implementation which takes a CSV file containing a
  molecule dataset of SMILES and target values into a visual graph dataset.

    * ``generate_molecule_dataset_from_csv_aqsoldb.py``: Generates the VGD for the AqSolDB dataset based
      on the CSV file from the remote repository

