import os
import pandas as pd
import numpy as np

ihs_files = os.listdir("D:\\iHS")

daf_cols_names = [
    "daf_ESN",
    "daf_GWD",
    "daf_LWK",
    "daf_MSL",
    "daf_YRI",
    "daf_ACB",
    "daf_ASW",
    "daf_CLM",
    "daf_MXL",
    "daf_PEL",
    "daf_PUR",
    "daf_CDX",
    "daf_CHB",
    "daf_CHS",
    "daf_JPT",
    "daf_KHV",
    "daf_CEU",
    "daf_FIN",
    "daf_GBR",
    "daf_IBS",
    "daf_TSI",
    "daf_BEB",
    "daf_GIH",
    "daf_ITU",
    "daf_PJL",
    "daf_STU",
]

stdIHS_cols_names = [
    "stdIHS_ESN",
    "stdIHS_GWD",
    "stdIHS_LWK",
    "stdIHS_MSL",
    "stdIHS_YRI",
    "stdIHS_ACB",
    "stdIHS_ASW",
    "stdIHS_CLM",
    "stdIHS_MXL",
    "stdIHS_PEL",
    "stdIHS_PUR",
    "stdIHS_CDX",
    "stdIHS_CHB",
    "stdIHS_CHS",
    "stdIHS_JPT",
    "stdIHS_KHV",
    "stdIHS_CEU",
    "stdIHS_FIN",
    "stdIHS_GBR",
    "stdIHS_IBS",
    "stdIHS_TSI",
    "stdIHS_BEB",
    "stdIHS_GIH",
    "stdIHS_ITU",
    "stdIHS_PJL",
    "stdIHS_STU",
]

ihs_files = os.listdir("D:\\iHS")
out_folder = "D:\\iHS\\iHS_mean"
os.makedirs(out_folder, exist_ok=True)

for file in ihs_files:
    file_path = os.path.join("D:\\iHS", file)
    df = pd.read_csv(file_path, sep="\t", comment="#", low_memory=False)

    # DAF
    daf = df["DAF"].str.split("|", expand=True)
    daf = daf.set_axis(daf_cols_names, axis=1)
    daf.replace({"NA": np.nan}, inplace=True)
    daf = daf.astype(dtype="float64")
    daf["mean_daf"] = daf.max(axis=1)

    # stdiHS
    stdIHS = df["stdIHS"].str.split("|", expand=True)
    stdIHS = stdIHS.set_axis(stdIHS_cols_names, axis=1)
    stdIHS.replace({"NA": np.nan}, inplace=True)
    stdIHS = stdIHS.astype(dtype="float64")
    stdIHS["mean_stdiHS"] = stdIHS.max(axis=1, skipna=True)

    # concat
    iHS_data = pd.concat(
        [df[["CHR", "POS", "RSNUM"]], daf["mean_daf"], stdIHS["mean_stdiHS"]], axis=1
    )

    # output filename
    base_name = os.path.splitext(file)[0]
    prefix = base_name.split(".")[0]
    output = os.path.join(out_folder, f"{prefix}_iHS_mean.csv")

    iHS_data.to_csv(output, index=False)
