# ParseCDI

An (unofficial) library for parsing the output of Crystal Disk Info.
Be sure to install Crystal Disk Info before trying to use.

# Installation
```
pip install parsecdi
```

# Live API Example
```
# Run as admin for best experience

In [1]: from parsecdi import CrystalDiskInfo

# This actually fetches info from Crystal Disk Info on the current system
In [2]: ds = CrystalDiskInfo.get().get_disks()
# If you wanted to parse an existing output file, use:
# ds = CrystalDiskInfo(None).get_disks(pathlib.Path(<FILE>))

In [3]: ds
Out[3]:
[<Disk - Samsung SSD 980 PRO 1TB - S5P2NG0NB05964V - 1000.2 GB>,
 <Disk - WDS100T3X0C-00SJG0 - 20379E802164 - 1000.2 GB>]

In [4]: d = ds[0]

In [5]: d.model
Out[5]: 'Samsung SSD 980 PRO 1TB'

In [6]: d.firmware
Out[6]: '5B2QGXA7'

In [7]: d.health.status
Out[7]: 'Good'

In [8]: d.health.percent
Out[8]: 87

In [9]: d.health.smart
Out[9]:
(DiskSMARTAttribute(id=1, name='Critical Warning', raw=0, current=None, worst=None, threshold=None),
 DiskSMARTAttribute(id=2, name='Composite Temperature', raw=325, current=None, worst=None, threshold=None),
 DiskSMARTAttribute(id=3, name='Available Spare', raw=100, current=None, worst=None, threshold=None),
 DiskSMARTAttribute(id=4, name='Available Spare Threshold', raw=10, current=None, worst=None, threshold=None),
 DiskSMARTAttribute(id=5, name='Percentage Used', raw=13, current=None, worst=None, threshold=None),
 DiskSMARTAttribute(id=6, name='Data Units Read', raw=151350782, current=None, worst=None, threshold=None),
 DiskSMARTAttribute(id=7, name='Data Units Written', raw=264526622, current=None, worst=None, threshold=None),
 DiskSMARTAttribute(id=8, name='Host Read Commands', raw=5047763158, current=None, worst=None, threshold=None),
 DiskSMARTAttribute(id=9, name='Host Write Commands', raw=7843108273, current=None, worst=None, threshold=None),
 DiskSMARTAttribute(id=10, name='Controller Busy Time', raw=19141, current=None, worst=None, threshold=None),
 DiskSMARTAttribute(id=11, name='Power Cycles', raw=663, current=None, worst=None, threshold=None),
 DiskSMARTAttribute(id=12, name='Power On Hours', raw=3451, current=None, worst=None, threshold=None),
 DiskSMARTAttribute(id=13, name='Unsafe Shutdowns', raw=36, current=None, worst=None, threshold=None),
 DiskSMARTAttribute(id=14, name='Media and Data Integrity Errors', raw=0, current=None, worst=None, threshold=None),
 DiskSMARTAttribute(id=15, name='Number of Error Information Log Entries', raw=0, current=None, worst=None, threshold=None))
```

See [https://csm10495.github.io/parsecdi/](https://csm10495.github.io/parsecdi/) for full API documentation.

## License
MIT License
