"""Generate publication tables and figures from collected CSV, without raw edits.

From the report folder: python prepare_assets.py
Uses bundled report data if present; otherwise copies collected data from parent.
"""

import csv
import hashlib
import json
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
for name in ("all_runs.csv", "scenario_summary.csv", "amat_sensitivity.csv"):
    if not (DATA / name).exists():
        shutil.copyfile(ROOT.parent / "results/BATCH01" / name, DATA / name)
if not (DATA / "environment.json").exists():
    env = json.loads((ROOT.parent / "evidence/ENVIRONMENT.json").read_text(encoding="utf-8"))
    # Preserve only reported version fields; never print machine-local locations.
    (DATA / "environment.json").write_text(json.dumps({k:env[k] for k in ("python","matplotlib","numpy")},indent=2),encoding="utf-8")
with (DATA / "scenario_summary.csv").open(encoding="utf-8-sig",newline="") as f: summary=list(csv.DictReader(f))
with (DATA / "all_runs.csv").open(encoding="utf-8-sig",newline="") as f: runs=list(csv.DictReader(f))
with (DATA / "amat_sensitivity.csv").open(encoding="utf-8-sig",newline="") as f: amat=list(csv.DictReader(f))
assert (len(runs),len(summary),len(amat))==(96,60,864)
DESIGNS=("D0","D1","D2","DAI-v1")
SCENARIOS=list(dict.fromkeys(row["scenario"] for row in summary))
def row(s,d):return next(r for r in summary if r["scenario"]==s and r["design"]==d)
def label(s):return s.replace("W2-1024","W2 1 KiB").replace("W2-4096","W2 4 KiB").replace("W2-16384","W2 16 KiB").replace("-"," ")
tables=ROOT/"tables";tables.mkdir(exist_ok=True)
text=[r"\begin{table}[htbp]\centering\small",r"\caption{Measured miss rates (\%). W4 random reports the mean of ten seeds; its sample standard deviation is zero for all designs. Other rows are deterministic cases.}\label{tab:results}",r"\begin{tabular}{lrrrr}\toprule",r"Scenario & D0 & D1 & D2 & \dai{}\\\midrule"]
for s in SCENARIOS:
    text.append(label(s)+" & "+" & ".join(f"{float(row(s,d)['miss_rate_mean'])*100:.3f}" for d in DESIGNS)+r"\\")
text += [r"\bottomrule\end{tabular}",r"\end{table}"]
(tables/"results.tex").write_text("\n".join(text)+"\n",encoding="utf-8")
text=[r"\begin{table}[htbp]\centering\small",r"\caption{Selected measured memory traffic (bytes). No final dirty-line flush is included.}\label{tab:traffic}",r"\begin{tabular}{lrr}\toprule",r"Scenario & D0 & \dai{}\\\midrule"]
for s in ("W1-read","W1-write","W3-N8","W3-N2048","W5-K8"):
    text.append(label(s)+" & "+" & ".join(f"{float(row(s,d)['traffic_bytes_mean']):,.0f}" for d in ("D0","DAI-v1"))+r"\\")
text += [r"\bottomrule\end{tabular}",r"\end{table}"]
(tables/"traffic.tex").write_text("\n".join(text)+"\n",encoding="utf-8")
env=json.loads((DATA/"environment.json").read_text(encoding="utf-8"))
text=[r"\begin{table}[htbp]\centering\small",r"\caption{Recorded execution and analysis software.}",r"\begin{tabular}{ll}\toprule",r"Component & Version / role\\\midrule",
      f"Python & {env['python'].split()[0]} / simulator and generator"+r"\\",
      f"Matplotlib & {env['matplotlib']} / figures"+r"\\",
      f"NumPy & {env['numpy']} / plot preparation"+r"\\",
      r"External simulator dependencies & None; standard library only\\",
      r"\bottomrule\end{tabular}",r"\end{table}"]
(tables/"environment.tex").write_text("\n".join(text)+"\n",encoding="utf-8")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
figdir=ROOT/"figures";figdir.mkdir(exist_ok=True)
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":10,"axes.spines.top":False,"axes.spines.right":False,"pdf.fonttype":42})
fig,ax=plt.subplots(figsize=(6.5,3.25));x=np.arange(3);width=.19
for j,(design,color) in enumerate(zip(DESIGNS,("#64748b","#2563eb","#16a34a","#dc2626"))):
    ax.bar(x+(j-1.5)*width,[float(row(f"W5-K{k}",design)["miss_rate_mean"])*100 for k in (2,4,8)],width,label=design,color=color)
ax.set_xticks(x,["2 blocks","4 blocks","8 blocks"]);ax.set_ylim(0,114);ax.set_ylabel("Measured miss rate (%)")
ax.set_xlabel("Competing blocks separated by 4 KiB");ax.legend(ncol=4,loc="upper center",fontsize=8,frameon=False)
ax.grid(axis="y",alpha=.2);ax.set_axisbelow(True);fig.tight_layout()
fig.savefig(figdir/"stress.pdf",bbox_inches="tight");fig.savefig(figdir/"stress.png",dpi=180,bbox_inches="tight");plt.close(fig)
# Verify selected claim values directly against the per-run table.
expected={"W1-read":.125,"W1-write":.125,"W3-N8":.01389,"W3-N32":.00379,"W3-N128":.00097,"W3-N512":.00024,"W3-N2048":.12537}
for s,v in expected.items():
    assert all(abs(float(row(s,d)["miss_rate_mean"])-v)<1e-12 for d in DESIGNS)
for k in (2,4,8):
    assert float(row(f"W5-K{k}","D0")["miss_rate_mean"])==1
    assert float(row(f"W5-K{k}","DAI-v1")["miss_rate_mean"])==0
for r in runs:
    assert int(r["accesses"])==100000
    assert int(r["memory_traffic_bytes"])==(int(r["line_fills"])+int(r["dirty_writebacks"]))*32
audit={"data_rows":{"runs":96,"summary":60,"amat":864},"numeric_claim_checks":"PASS",
       "data_sha256":{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in DATA.glob("*.csv")}}
(ROOT/"data_checks.json").write_text(json.dumps(audit,indent=2)+"\n",encoding="utf-8")
source=(ROOT/"main.tex").read_text(encoding="utf-8")
counts={}
for key,prose in re.findall(r"% COUNT-BEGIN (\w+)\n(.*?)% COUNT-END \1",source,re.S):
    prose=re.sub(r"\\begin\{(table|figure|align)\}.*?\\end\{\1\}"," ",prose,flags=re.S)
    prose=re.sub(r"\\(?:cite|ref|label)\{[^}]*\}"," ",prose)
    prose=re.sub(r"\\(?:subsection|section)\{[^}]*\}"," ",prose)
    prose=re.sub(r"\\[a-zA-Z]+\*?(?:\[[^]]*\])?", " ", prose)
    counts[key]=len(re.findall(r"\b[\w]+(?:[-'][\w]+)*\b",prose))
(ROOT/"word_counts.json").write_text(json.dumps(counts,indent=2),encoding="utf-8")
print("Generated tables/figure and checked 96 result rows; approximate prose word counts:",counts)
