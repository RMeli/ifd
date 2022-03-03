#/bin/bash

# Perform docking with rigid and flexible residues using GNINA

exhaustiveness=8

cpus=8

while read line; do
  rec=$(echo ${line} | awk -F "," '{print $1}')
  lig=$(echo ${line} | awk -F "," '{print $4}')

  flexres=$(echo ${line} | awk -F "," '{print $7}' | sed 's#/#,#g')

  echo ${rec} ${lig}
  echo ${flexres}

  dir="data/${rec}_${lig}"
  outdir="docking/residues_exhaustiveness${exhaustiveness}/${rec}_${lig}"

  mkdir -p ${outdir}

  outprefix=${outdir}/${rec}_${lig}

  if [ -z "${flexres}" ]
  then
    singularity run --nv --app gnina singularity/gnina.sif \
      -r ${dir}/${rec}.pdb -l ${dir}/${lig}_lig.pdb \
      --autobox_ligand ${dir}/${rec}_lig.pdb \
      --seed 42 --exhaustiveness ${exhaustiveness} --cpu ${cpus} \
      -o ${outprefix}_flex.pdb --out_flex ${outprefix}_flex_residues.pdb \
      | tee ${outprefix}_flex.log
  else
    singularity run --nv --app gnina singularity/gnina.sif \
      -r ${dir}/${rec}.pdb -l ${dir}/${lig}_lig.pdb \
      --autobox_ligand ${dir}/${rec}_lig.pdb \
      --flexres ${flexres} \
      --seed 42 --exhaustiveness ${exhaustiveness} --cpu ${cpus} \
      -o ${outprefix}_flex.pdb --out_flex ${outprefix}_flex_residues.pdb \
      | tee ${outprefix}_flex.log
  fi

  python -m spyrmsd ${dir}/${lig}_lig.pdb ${outprefix}_flex.pdb > ${outprefix}_flex.rmsd

  singularity run --nv --app gnina singularity/gnina.sif \
    -r ${dir}/${rec}.pdb -l ${dir}/${lig}_lig.pdb \
    --autobox_ligand ${dir}/${rec}_lig.pdb \
    --seed 42 --exhaustiveness ${exhaustiveness} --cpu ${cpus} \
    -o ${outprefix}.pdb \
    | tee ${outprefix}.log

  python -m spyrmsd ${dir}/${lig}_lig.pdb ${outprefix}.pdb > ${outprefix}.rmsd

done < <(tail -n +2 IFDdata.csv)