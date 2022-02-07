import prody
import pandas as pd

import os

df = pd.read_csv("IFDdata.csv")

print(df)

for i, r in df.iterrows():
    dirname = r.rec_pdb + "_" + r.lig_pdb
    os.makedirs(dirname, exist_ok=True)

    rec_pdb_file = prody.fetchPDB(r.rec_pdb, chain=r.rec_chid, folder=dirname)
    lig_pdb_file = prody.fetchPDB(r.lig_pdb, folder=dirname)

    rec_pdb = prody.parsePDB(rec_pdb_file)
    lig_pdb = prody.parsePDB(lig_pdb_file)

    # Compute structure alignment
    for cutoff in range(90, 0, -10):
        matches = prody.matchChains(
            rec_pdb,
            lig_pdb,
            subset="backbone",
            seqid=cutoff,
            overlap=cutoff,
            pwalign=True,
        )

        if matches is not None:
            break

    # Sort matches and get best one
    matches.sort(key=lambda t: t[2])
    match = matches[0]

    # Superimpose structures
    t = prody.calcTransformation(match[1], match[0])
    t.apply(lig_pdb)

    # Receptor for docking (including ions/metals)
    rec = rec_pdb.select(
        f"(protein and not hetatm and not water) or (ion within 5 of (hetatm and resname {r.rec_lig_id}))"
    )
    prody.writePDB(os.path.join(dirname, f"{r.rec_pdb}.pdb"), rec)

    # Cognate ligand of receptor for docking
    # Needed to define the binding site
    autoboxlig = rec_pdb.select(
        f"hetatm and resname {r.rec_lig_id} and chain {r.rec_chid}"
    )
    prody.writePDB(os.path.join(dirname, f"{r.rec_pdb}_lig.pdb"), autoboxlig)

    # Ligand for docking
    lig = lig_pdb.select(f"hetatm and resname {r.lig_id} and chain {r.lig_chid}")
    prody.writePDB(os.path.join(dirname, f"{r.lig_pdb}_lig.pdb"), lig)
