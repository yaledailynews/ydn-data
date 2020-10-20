import pandas as pd


def filter_professors(row):
    if "MED" in row["department"] and row["title"].count("Professor") == 1:
        return False
    return True


professors = pd.read_csv("output.csv")
professors = professors[professors.apply(filter_professors, axis=1)]

print("loaded professors")

contributions = pd.read_csv("all_contributions.txt", names=[
"CMTE_ID","AMNDT_IND","RPT_TP","TRANSACTION_PGI","IMAGE_NUM","TRANSACTION_TP","ENTITY_TP","NAME","CITY","STATE","ZIP_CODE","EMPLOYER","OCCUPATION","TRANSACTION_DT","TRANSACTION_AMT","OTHER_ID","TRAN_ID","FILE_NUM","MEMO_CD","MEMO_TEXT","SUB_ID"
])

print("loaded contributions")

yale_contributions = professors.merge(contributions, left_on="name", right_on="NAME")
del contributions
del professors
print("merged contributions")


cm = pd.read_csv("cm.txt", delimiter="|").drop_duplicates(subset=["CMTE_ID"])

yale_contributions = yale_contributions.merge(cm, on="CMTE_ID")

del cm
print("merged in committee data")

yale_contributions["CMTE_PTY_AFFILIATION"] = yale_contributions.apply(lambda x: "DEM" if x["CMTE_NM"] == "ACTBLUE" else x["CMTE_PTY_AFFILIATION"], axis=1)

print("updated ActBlue")

yale_contributions["TRANSACTION_DT"] = pd.to_datetime(yale_contributions["TRANSACTION_DT"], format="%m%d%Y")

yale_contributions.to_csv("yale_contributions.csv", index=False)