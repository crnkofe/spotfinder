# spotfinder
CapsuleHack'20 parking spot finder concepts

To run the scripts make sure to install Python 3 and requirements.txt

```
mkvirtualenv --python=/usr/bin/python3 spotfinder
workon spotfinder
pip install -r requirements.txt
```

To run an estimation of CO2 savings do
```
python3 estimate_emissions.py
```

To run an algorithm to find nearest parking spot go with
```
python3 finder.py micro_lot.txt
```
