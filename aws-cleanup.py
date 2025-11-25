# ===============================================
# AWS CLEANUP SCRIPT - FINAL - DELETES - WINDOWS SAFE
# ===============================================

import boto3
from datetime import datetime, timedelta, timezone

DRY_RUN = True                    # SET TO False = actually delete
DAYS_OLD = 60
REGIONS = ['us-east-1']
PROTECT_TAG = "DoNotDelete"

print("\n=== AWS ORPHANED RESOURCE CLEANUP ===")
print("LIVE MODE - RESOURCES WILL BE DELETED!" if not DRY_RUN else "DRY RUN - nothing will be deleted")
print()

def main():
    for region in REGIONS:
        print("Region:", region)
        print("-" * 60)
        ec2 = boto3.client('ec2', region_name=region)

        # 1. Unattached EBS volumes
        volumes = ec2.describe_volumes(Filters=[{'Name': 'status', 'Values': ['available']}])['Volumes']
        for v in volumes:
            if any(tag.get('Key') == PROTECT_TAG for tag in v.get('Tags', [])):
                print("SKIPPED (protected):", v['VolumeId'])
                continue
            print("DELETING unattached volume:", v['VolumeId'], f"({v['Size']} GB)")
            if not DRY_RUN:
                ec2.delete_volume(VolumeId=v['VolumeId'])
                print("   DELETED successfully")

        # 2. Unused Elastic IPs
        addresses = ec2.describe_addresses()['Addresses']
        for e in addresses:
            if e.get('InstanceId') or e.get('NetworkInterfaceId'):
                continue
            if any(tag.get('Key') == PROTECT_TAG for tag in e.get('Tags', [])):
                continue
            print("RELEASING unused Elastic IP:", e['PublicIp'])
            if not DRY_RUN:
                ec2.release_address(AllocationId=e['AllocationId'])
                print("   RELEASED successfully")

        # 3. Old snapshots
        snapshots = ec2.describe_snapshots(OwnerIds=['self'])['Snapshots']
        cutoff = datetime.now(timezone.utc) - timedelta(days=DAYS_OLD)
        for s in snapshots:
            if any(tag.get('Key') == PROTECT_TAG for tag in s.get('Tags', [])):
                continue
            st = s['StartTime']
            if st.tzinfo is None:
                st = st.replace(tzinfo=timezone.utc)
            if st < cutoff:
                print("DELETING old snapshot:", s['SnapshotId'], "(created", st.date(), ")")
                if not DRY_RUN:
                    ec2.delete_snapshot(SnapshotId=s['SnapshotId'])
                    print("   DELETED successfully")

        print()

    print("=== ALL DONE ===")

if __name__ == "__main__":
    main()
