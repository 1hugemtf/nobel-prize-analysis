"""Execute the notebook from scratch and verify the Nobel analysis and charts."""
from pathlib import Path
import sys
import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager

root = Path(__file__).resolve().parent
nb = nbformat.read(root / "notebook.ipynb", as_version=4)
nbformat.validate(nb)
for cell in nb.cells:
    if cell.cell_type == "code":
        cell.outputs = []
        cell.execution_count = None
nb.cells.append(nbformat.v4.new_code_cell("\nassert len(nobel)==911 and nobel.year.min()==1901 and nobel.year.max()==2016\nassert not nobel.duplicated(['laureate_id','year','category']).any()\nassert nobel.laureate_id.nunique()==904\nassert len(nobel[['year','category']].drop_duplicates())==579\nassert len(people)==885 and len(organizations)==26 and people.laureate_id.nunique()==881\nassert nobel.loc[nobel.laureate_id.isin(correction_ids),'source_laureate_type'].eq('Organization').all()\nassert nobel.loc[nobel.laureate_id.isin(correction_ids),'laureate_type'].eq('Individual').all()\nassert int((raw.laureate_type!=nobel.laureate_type).sum())==4\nnp.testing.assert_allclose(nobel.groupby(['year','category']).share.sum(),1)\nassert category_counts.sum()==len(nobel)\nassert us_share.Eligible_records.sum()==len(birth_known)\nassert female_share.Eligible_records.sum()==len(sex_known)\nassert female_share.Female_records.sum()==49\nassert us_share.Proportion.between(0,1).all() and female_share.Proportion.between(0,1).all()\nassert len(repeat_counts)==6 and repeat_counts.loc[482]==3\nassert first_female.year.tolist()==[1903] and first_female.laureate_id.tolist()==[6]\nassert len(aged)==883 and aged.approx_age.between(0,110).all()\nassert youngest.full_name.tolist()==['Malala Yousafzai'] and youngest.approx_age.tolist()==[17]\nassert oldest.full_name.tolist()==['Leonid Hurwicz'] and oldest.approx_age.tolist()==[90]\nassert age_summary.Records.sum()==len(aged)\nassert ('Economics',1900) not in female_share.index\nfor name in ['awards_and_birth_countries.png','us_born_share.png','female_representation.png','award_age_by_category.png']:\n assert Path(name).is_file() and Path(name).stat().st_size>10000\n"))
km = KernelManager(kernel_name="python3")
km.kernel_spec.argv = [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"]
client = NotebookClient(nb, km=km, timeout=180,
    resources={"metadata": {"path": str(root)}})
try:
    client.execute()
finally:
    if km.has_kernel:
        km.shutdown_kernel(now=True)
nb.cells.pop()
nbformat.write(nb, root / "notebook.ipynb")
print("PASS: notebook executed from cleared outputs; Nobel analysis and chart checks passed.")
