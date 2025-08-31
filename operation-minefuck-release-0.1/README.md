# Operation Minefuck  
**Don’t get mined. Mine back.**  

Surveillance capitalism treats you like a free-range data cow.  
This project flips the script: instead of being farmed for your clicks and habits,  
you **harvest your own metadata**, curate it into a profile *you* control,  
and only accept bids from advertisers on **your terms**.  

Part prank. Part protest. Part prototype for a weirder, freer internet.  

## Quick Start
```bash
cd prototype
python -m venv .venv
source .venv/bin/activate  # Windows: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python curate_profile.py
FLASK_APP=server.py flask run --host 0.0.0.0 --port 8787
```
Open http://localhost:8787/profile
