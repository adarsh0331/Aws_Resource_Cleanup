<img width="940" height="627" alt="image" src="https://github.com/user-attachments/assets/44cb29df-a023-4560-8e40-2a619df1fe5f" />

# AWS Resource Cleanup Script  
**Delete unused EBS volumes, Elastic IPs & old snapshots → Save money instantly**

Works 100% on **Windows, macOS, and Linux** ·

---

## What It Deletes (when LIVE mode is on)

| Resource                | Condition                                      | Monthly Cost if Forgotten |
|-------------------------|--------------------------------------------------|-----------------------------|
| Unattached EBS volumes  | Status = `available`                             | ~$0.10 per GB              |
| Unused Elastic IPs      | Not attached to anything                         | $3–$5 per IP               |
| Old EBS snapshots       | Older than 60 days (you can change this)         | ~$0.05 per GB              |

---

## FULL WINDOWS SETUP + RUN 

### Step 1: Install Python on Windows (one-time only)

1. Go to → https://www.python.org/downloads/
2. Click the big yellow button **"Download Python 3.12"** (or newer)
3. Run the downloaded `.exe` file
4. **IMPORTANT**: Check the box **"Add Python to PATH"** at the bottom
5. Click **"Install Now"**
6. Wait → Click **"Close"**

Done! Python is now installed.

### Step 2: Open Terminal (Command Prompt or Git Bash)

- Press `Win + R` → type `cmd` → Enter  
  OR just use Git Bash (you already have it)

### Step 3: Install the AWS library

Copy-paste this one command and press Enter:

```bash
pip install boto3
```

You’ll see it downloading and installing.

### Step 4: Set up your AWS credentials (one-time)

Run these 4 lines one by one (replace with your own keys from AWS IAM):

```bash
aws configure set aws_access_key_id AKIAxxxxxxxxxxxxxxxx
aws configure set aws_secret_access_key xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
aws configure set region us-east-1
aws configure set output json
```

(If you don’t have keys yet → go to AWS Console → IAM → Users → your user → Security credentials → Create access key → CLI)

### Step 5: Save the script

1. Copy the file `aws-cleanup.py` (the final version I gave you)  
2. Save it on your **Desktop**

### Step 6: First run — 100% SAFE preview

In terminal, run:

```bash
cd Desktop
python aws-cleanup.py
```

You’ll see everything that **would** be deleted. Nothing is touched yet.

### Step 7: Actually delete (when you're ready)

1. Open `aws-cleanup.py` in Notepad
2. Change this line near the top:
   ```python
   DRY_RUN = True
   ```
   → to →
   ```python
   DRY_RUN = False
   ```
3. Save the file
4. Run again:
   ```bash
   python aws-cleanup.py
   ```

Your unused resources are now **gone forever** and you stop paying for them immediately.

---

## Configuration (top of the script)

```python
DRY_RUN = False          # False = really delete
DAYS_OLD = 60            # Delete snapshots older than 60 days
REGIONS = ['us-east-1']  # Add more regions if you use them
PROTECT_TAG = "DoNotDelete"  # Tag anything important with this
```

**Pro tip**: Tag anything you never want deleted with  
Key: `DoNotDelete` → Value: `true`

---

## Example Output (LIVE mode)

```
=== AWS ORPHANED RESOURCE CLEANUP ===
LIVE MODE - RESOURCES WILL BE DELETED!

Region: us-east-1
------------------------------------------------------------
DELETING unattached volume: vol-06937f1640164adf6 (2 GB)
   DELETED successfully

=== ALL DONE ===
```

---

## Typical First-Run Savings

| Forgotten Resource          | Cost Before | Cost After |
|-----------------------------|-------------|------------|
| 3 × 8 GB unattached volumes | ~$2.40      | $0         |
| 2 unused Elastic IPs        | ~$10        | $0         |
| 100 GB old snapshots        | ~$5         | $0         |
| **Total monthly savings**   | **~$17+**   |            |

Many people save **$50–$500/month** on their very first run.

---

## Safety Checklist (always do this)

1. First run → `DRY_RUN = True`
2. Review the list
3. Tag anything important with `DoNotDelete`
4. Then switch to `DRY_RUN = False`

You’re now an AWS cost-saving hero

Run it monthly and keep your bill clean!
