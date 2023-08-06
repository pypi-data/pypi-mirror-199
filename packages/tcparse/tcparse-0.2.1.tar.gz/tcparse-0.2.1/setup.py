# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tcparse']

package_data = \
{'': ['*']}

install_requires = \
['qcelemental>=0.25.1']

entry_points = \
{'console_scripts': ['tcparse = tcparse.cli:main']}

setup_kwargs = {
    'name': 'tcparse',
    'version': '0.2.1',
    'description': 'A package for parsing TeraChem file outputs into structured MolSSI data objects.',
    'long_description': '# tcparse\n\nA library for parsing TeraChem output files into structured MolSSI data objects.\n\n## ✨ Basic Usage\n\n- Installation:\n\n  ```sh\n  python -m pip install tcparse\n  ```\n\n- Parse files into `AtomicResult` or `FailedOperation` objects with a single line of code.\n\n  ```python\n  from tcparse import parse\n\n  result = parse("/path/to/tc.out")\n  ```\n\n- If your `xyz` file no longer exists where `tc.out` specifies (the `XYZ coordinates` line), `parse` will raise a `FileNotFoundError`. You can pass `ignore_xyz=True` and `parse` will use a dummy hydrogen molecule instead. The correct values from `tc.out` will be parsed; however, `result.molecule` will be the dummy hydrogen.\n\n  ```python\n  from tcparse import parse\n\n  result = parse("/path/to/tc.out", ignore_xyz=True)\n  print(result) # Real results from tc.out\n  print(result.molecule) # Dummy hydrogen molecule\n  ```\n\n- The `result` object will be either an `AtomicResult` or `FailedOperation`. Run `dir(result)` inside a Python interpreter to see the various values you can access. A few prominent values are shown here as an example:\n\n  ```python\n  from tcparse import parse\n\n  result = parse("/path/to/tc.out")\n\n  if result.success:\n      # result is AtomicResult\n      result.driver # "energy", "gradient", or "hessian"\n      result.model # Method and basis\n      result.return_result # Core value from the computation. Will be either energy or grad/Hess matrix\n      result.properties # Collection of computed properties. Two shown below.\n      result.properties.return_energy # Available for all calcs\n      result.properties.return_gradient # Available for grad/Hess calcs\n      result.molecule # The molecule used for the computation\n      result.stdout # The full TeraChem stdout\n      result.provenance # Provenance data for the computation (TeraChem version)\n  else:\n      # result is FailedOperation\n      result.error # ComputeError object describing error\n      result.input_data # Basic data about the inputs supplied, does NOT include keywords\n      result.error.error_message # Parsed error message from TeraChem stdout\n      result.error.extras[\'stdout\'] # Full TeraChem stdout\n  ```\n\n- Parsed results can be written to disk like this:\n\n  ```py\n  with open("myresult.json", "w") as f:\n      f.write(result.json())\n  ```\n\n- And read from disk like this:\n\n  ```py\n  from qcelemental.models import AtomicResult, FailedOperation\n\n  successful_result = AtomicResult.parse_file("myresult.json")\n  failed_result = FailedOperation.parse_file("myfailure.json")\n  ```\n\n- You can also run `tcparse` from the command line like this:\n\n  ```sh\n  tcparse -h # Get help message for cli\n\n  tcparse ./path/to/tc.out > myoutput.json # Parse TeraChem stdout to json\n\n  tcparse --ignore_xyz ./path/to/tc.out > myoutput.json # Ignore the XYZ file in the TeraChem stdout. Helpful in case the XYZ file is not longer available in the location specified in the file.\n  ```\n\n## 🤩 Next Steps\n\nThis package will be integrated into [QCEngine](https://github.com/MolSSI/QCEngine) soon. So if you like getting your TeraChem data in this format, you\'ll be able to drive TeraChem from pure python like this:\n\n```python\nfrom qcelemental.models import Molecule, AtomicInput\nfrom qcengine import compute\n\nmolecule = Molecule.from_file("mymolecule.xyz")\natomic_input = AtomicInput(\n    molecule=molecule,\n    driver="gradient", # "energy" | "gradient" | "hessian"\n    model={"method": "b3lyp", "basis": "6-31gs"},\n    keywords={"restricted": True, "purify": "no"} # Keywords are optional\n    )\n\n# result will be AtomicResult or FailedOperation\nresult = compute(atomic_input, "terachem")\n```\n\n## 💻 Contributing\n\nIf there\'s data you\'d like parsed from TeraChem output files, please open an issue in this repo explaining the data items you\'d like parsed and include an example output file containing the data, like [this](https://github.com/mtzgroup/tcparse/issues/2).\n\nIf you\'d like to add a parser yourself see the docstring in `tcparse.parsers` for a primer and see the examples written in the module. Adding a parser for new data is quick and easy :)\n',
    'author': 'Colton Hicks',
    'author_email': 'github@coltonhicks.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
