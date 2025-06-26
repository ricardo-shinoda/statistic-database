# This is a financial control repository

#### To run this project first install all the dependencies by running, from the root:

`pip install -r requirements.txt`

#### To update Account_mvt (all the movements from the account)

- First activate .venv (source .venv/bin/activate)
- Download the file from the app (do it monthly)
- Rename to: account_mvt.pdf
- Move to /home/ricardo/code/statistic
- run: `python3 converter_pdf_json.py (from the src)`
- rename the output to: yyyy-mm.json
- Move file renamed to src/account_mvt/json

### [control4.py] To update Credit Card invoices:

### This code does:

- extract from .zip
- rename Controle file
- move Controle to this repository
- run the code

- From the C6 App, download the invoice .csv file to my /home/Download (From email)
- Download the latest version of Controle.xsls from G-drive
- Rename Controle file to just Controle.xsls
  `mv /home/ricardo/Downloads/Controle*.xlsx /home/ricardo/Downloads/Controle.xlsx`
- Then move to the project
  `mv /home/ricardo/Downloads/Controle.xlsx /home/ricardo/code/statistic/src`
- Don´t forget to update variable "month" on control.py -"yyyy-mm" line
  `python3 control4.py`

### The same as above but all together

    - Delete Control.xmls file from this repository
    - From /drive/statistic/ download the latest Controle.xmls file
        - leave it at the Download folder.
    - Download the invoice from the app to email and fom the email to this computer (Download folder)
    - on control4.py file, rename the month.
    - run the commands below

```shell
mv /home/ricardo/Downloads/Controle*.xlsx /home/ricardo/Downloads/Controle.xlsx
mv /home/ricardo/Downloads/Controle.xlsx /home/ricardo/code/statistic/src
python3 control4.py
```

### [control3.py] To do the same steps as control4 but without converting .zip file

Good to use if I manually convert the file, also good to test correct file that are already on the DESKTOP

```shell
mv /home/ricardo/Downloads/Controle*.xlsx /home/ricardo/Downloads/Controle.xlsx
mv /home/ricardo/Downloads/Controle.xlsx /home/ricardo/code/statistic/src
python3 control3.py
```

### [control2.py] To convert .csv to .json and .xlsx

get the .csv from bank, open with text editor, save as on /Downloads/invoice/invoice.csv

```shell
python3 control2.py.
```

- For the next updates, don't forget to remove:
  - the file FATURA-CSV.csv on /Download
  - Controle.xlsx on /src

#### To update sql postgres

- After the step above is done, update line variable month (combined or just the single)
- Run:

```shell
python3 sql_query.py
```

## Files Breakdown:

Conversion Files (convert various files into .json or .xlsx)

    - converter_csv_json.py
    Reads invoice.csv file from repo and convert to .json and save it as "output.json" on /src/credit_card/json

    - convert_csv_xlsx.py
    Does the same as above, but convert to .xlsx and prepare to use on Controle.xlsx.

Upload Files

    - drive_upload_tab.py
    Take especific file from credict_card/xlsx/ folder and save it on /src/Controle.xlsx and upload it to G-drive (Statistic folder)

Download File

    - donwload_repo.py
    Download file from /Downloads/invoice to repo also renaming it.

Search Files

    - search for files with .csv on /Downloads/invoice and convert it to .xlsx
