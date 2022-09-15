# NGSS_download

A hackish script to download NGSS camera recordings. Use it at your own risk!

## Setup Conda Environment

```
conda env create -f environment.yml
conda activate ngss
python main.py test_glob date
python main.py test_glob hour
```

## Usage:
Find the IP address in the browser URL, something like `192.168.1.5`.
Let's call this `<x.x.x.x>`, and you should replace `<x.x.x.x>` with actual ip address you found.
You can put the address in `config.yml` to avoid inputing it in command line every time.

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

### Test Auto-download

```
python main.py test_auto_download 20220402 --ip=<x.x.x.x>
```
And monitor the downloading folder and the proxy software.
This will start to download all videos of the previous day 20220401 after 1 min delay.
