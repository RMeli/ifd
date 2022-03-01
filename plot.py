import pandas as pd
import os

import seaborn as sns
from matplotlib import pyplot as plt


prefix = "flexdist3.5_exhaustiveness8"
# prefix = "flexdist3.5_exhaustiveness64"
# prefix = "flexdist4.5_exhaustiveness8"
# prefix = "flexdist4.5_exhaustiveness64"

wdir = os.path.join("docking", prefix)

df = pd.read_csv("IFDdata.csv")

rmsds = pd.DataFrame(columns=["rigid", "flexible", "id"])


for i, r in df.iterrows():
    dirname = r.rec_pdb + "_" + r.lig_pdb
    print(dirname)

    rigid = pd.read_csv(
        f"{wdir}/{dirname}/{dirname}.rmsd", header=None, index_col=None, names=["rmsd"]
    )
    flex = pd.read_csv(
        f"{wdir}/{dirname}/{dirname}_flex.rmsd",
        header=None,
        index_col=None,
        names=["rmsd"],
    )

    rmsds = rmsds.append(
        {
            "rigid": rigid.iloc[0]["rmsd"],
            "flexible": flex.iloc[0]["rmsd"],
            "id": r.rec_pdb.upper() + "-" + r.lig_pdb.upper(),
        },
        ignore_index=True,
    )

ifd = pd.read_csv("IFDresults.csv").rename(columns={"rigid": "glide"})
ifd["id"] = ifd["rec"].str.upper() + "-" + ifd["lig"].str.upper()

rmsds = pd.merge(rmsds, ifd.drop(columns=["lig", "rec"]), on="id")

print(rmsds)

rmsds.to_csv(f"{wdir}/IFDrmsds-{prefix}.csv", index=False, float_format="%.5f")

rmsds_melted = rmsds.melt(
    value_vars=["rigid", "flexible", "ifd", "glide"],
    id_vars="id",
    var_name="Method",
    value_name="rmsd",
)

print(rmsds_melted)


def handleplot(data, values, colors=None):
    melted = data.melt(
        value_vars=values, id_vars="id", var_name="Method", value_name="rmsd"
    )

    g = sns.relplot(
        data=melted, x="rmsd", y="id", hue="Method", kind="scatter", palette=colors
    )

    plt.axvline(2.0, color="grey", linestyle="--")
    plt.xlim(0, None)
    plt.ylabel(None)
    plt.xlabel("Ligand RMSD")
    for i, (x1, x2) in data[values].iterrows():
        plt.hlines(i, x1, x2, color="grey", linestyle="-", zorder=-1)


plt.figure()
handleplot(rmsds, ["flexible", "ifd"])
plt.savefig(os.path.join(wdir, "rmsd-fVSifd.png"))
handleplot(rmsds, ["flexible", "rigid"])
plt.savefig(os.path.join(wdir, "rmsd-fVSr.png"))
