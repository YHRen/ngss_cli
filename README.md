# NGSS_download

A hackish script to download NGSS camera recordings. Use it at your own risk!

## Setup Conda Environment

```
conda env create -f environment.yml
conda activate ngss
python main.py test date
python main.py test hour
```

## Usage:
Find the IP address in the browser URL, something like `192.168.1.5`.
Let's call this `<x.x.x.x>`, and you should replace `<x.x.x.x>` with actual ip address you found.


### List Dates with Recordings

```
python main.py list --ip=<x.x.x.x>
```

**Replace the IP address `<x.x.x.x>` you found in your browser URL.**

### List Recodings within a Day

Pick a date from previous list, say, 20220401.
```
python main.py list 20220401 --ip=<x.x.x.x>
```
**Replace the IP address `<x.x.x.x>` you found in your browser URL.**

### Download All Recordings of a Day

Pick a date from previous list, say, 20220401.
```
python main.py download 20220401 --ip=<x.x.x.x>
```
**Replace the IP address `<x.x.x.x>` you found in your browser URL.**

### Continuously Downloading All Recordings of Previous Day at 2 AM

```
python main.py auto-download --ip=<x.x.x.x>
```
**Replace the IP address `<x.x.x.x>` you found in your browser URL.**
