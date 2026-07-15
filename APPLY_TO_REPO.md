# Applying this scaffold to the GitHub repository

From a local clone of `jltobias/Cross-Border-Ebola-Risk-Mapping-Prototype`:

```bash
unzip Cross-Border-Ebola-Risk-Mapping-Prototype-notebook-scaffold.zip -d scaffold
rsync -av scaffold/ ./

git checkout -b notebook-ecological-niche-risk-scaffold
git add .
git commit -m "Add Ebola ecological niche risk mapping notebook scaffold"
git push -u origin notebook-ecological-niche-risk-scaffold
```

Then open a pull request into `main`.

## Smoke test

```bash
conda env create -f environment.yml
conda activate cberm-ebola-risk
pip install -e .
python scripts/build_layer_catalog.py --gis-root GIS --out data/interim/layer_inventory.csv
python scripts/create_synthetic_demo_data.py
python scripts/run_synthetic_risk_demo.py
pytest
jupyter lab
```

If the current environment cannot install the package because it has no internet,
you can still run the tests against the source tree:

```bash
PYTHONPATH=src pytest
```
