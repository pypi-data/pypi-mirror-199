```python
import os
import sys
os.system(f'{sys.executable} -m pip install auto-env-config')
```
### Use requirements.txt
```python
import aec
aec.install('requirements.txt')
```
### Use config
```json
{
  "pip_index": "https://pypi.org/simple",
  "packages": [
    {
      "name": "numpy",
      "version": "1.22.0"
    }
  ],
  "files": [
    {
      "path": "/data",
      "nt_command": "mkdir -p /data"
    },
    {
      "path": "/data/requirements.txt",
      "posix_command": "echo numpy==1.22.0 > /data/requirements.txt"
    }
  ],
  "script": [
    {
      "command": "python -m pip install -r requirements.txt"
    }
  ]
}
```
```python
import aec
aec.install('install.config.json')
```
