# Combines source files from different years into a single file. Reformats
# names while doing so.
import csv
import sys
csv.field_size_limit(sys.maxsize)
from tqdm import tqdm
filenames = ["itcont_2013_2014.txt", "itcont_2015_2016.txt",
             "itcont_2017_2018.txt", "itcont_2019_2020.txt"]
headers = [
    "CMTE_ID", "AMNDT_IND", "RPT_TP", "TRANSACTION_PGI", "IMAGE_NUM",
    "TRANSACTION_TP", "ENTITY_TP", "NAME", "CITY", "STATE", "ZIP_CODE",
    "EMPLOYER", "OCCUPATION", "TRANSACTION_DT", "TRANSACTION_AMT", "OTHER_ID",
    "TRAN_ID", "FILE_NUM", "MEMO_CD", "MEMO_TEXT", "SUB_ID"
]

writer = csv.DictWriter(open("all_contributions.txt", "w"), fieldnames=headers)
writer.writeheader()

for filename in filenames:
    f = open("source_files/" + filename)
    reader = csv.DictReader(f, fieldnames=headers, delimiter="|")
    for row in tqdm(reader):
        if row["STATE"] == "CT" or "YALE" in row["EMPLOYER"]:
            try:
                lastname, firstname = row["NAME"].title().split(", ", maxsplit=1)
                row["NAME"] = firstname + " " + lastname
                writer.writerow(row)
            except ValueError:
                pass
    f.close()
    print("done with " + filename)