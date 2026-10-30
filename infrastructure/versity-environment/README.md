# Versity S3 environment

This pattern builds one AlmaLinux VM on Condenser running [Versity Gateway](https://github.com/versity/versitygw) (versitygw). Versity Gateway is an S3-compatible object store. It stores your objects as ordinary files on the VM's 75 GiB data disk, mounted at `/data`.

Once it is running you get:

- **S3 endpoint:** `https://<username>-s3.comp0235.condenser.arc.ucl.ac.uk`
- **Web UI:** `https://<username>-s3.comp0235.condenser.arc.ucl.ac.uk/ui/`

The Web UI is served from the same address as the S3 API, so your browser talks to a single site and there are no cross-origin (CORS) problems.

## Before you start

Run every command below on your CNC VM, from this directory. The inventory script and the playbooks read Terraform's outputs from here.

```bash
cd ~/engineering-for-datascience/infrastructure/versity-environment
```

You need:

- Terraform set up to reach Condenser, as for the other environments in `infrastructure/`.
- An SSH key uploaded to Rancher, with its private half on the CNC VM.
- The Ansible collections used for the disk setup:

```bash
ansible-galaxy collection install community.general ansible.posix
```

## 1. Create the VM

```bash
terraform init
terraform apply -var username=<ucl-id> -var keyname=<rancher-key-name>
```

`username` is your UCL ID. `keyname` is the name of your SSH key in Rancher. Neither has a default, so Terraform asks for them if you leave out `-var`. To save typing them every time, put them in a `terraform.tfvars` file in this directory (git ignores it):

```hcl
username = "<ucl-id>"
keyname  = "<rancher-key-name>"
```

## 2. Install the gateway

```bash
ansible-playbook -i ./generate_inventory.py -u almalinux \
  --private-key ~/.ssh/<your-key> full.yaml
```

This updates the VM and reboots it. It then formats and mounts the data disk, and installs and starts versitygw. It takes several minutes. Running it again is safe: it reboots the VM, but it won't reformat the data disk.

## 3. Log in to the Web UI

```bash
terraform output -raw webui_url
cat .versitypass
```

Open the Web UI address in your browser. Sign in with access key `administrator` and the password from `.versitypass`. The S3 endpoint is already filled in on the sign-in page.

The first playbook run creates `.versitypass`. It is the root password for your gateway, so keep it safe. Git ignores it.

## 4. Optional: load British Library data

`britishlibrary.yaml` copies zip archives from the course bucket (`https://s3.ds4eng.condenser.arc.ucl.ac.uk/britishlibrary/`) into a bucket called `britishlibrary` on your gateway. Run it after `full.yaml`:

```bash
ansible-playbook -i ./generate_inventory.py -u almalinux \
  --private-key ~/.ssh/<your-key> britishlibrary.yaml
```

By default it loads only `1510_1699.zip`, the smallest archive. To load others, pass a list of file names:

```bash
ansible-playbook -i ./generate_inventory.py -u almalinux \
  --private-key ~/.ssh/<your-key> britishlibrary.yaml \
  -e '{"britishlibrary_files": ["1510_1699.zip", "1810_1819.zip"]}'
```

The whole collection is about 0.5 TB, but the data disk is only 75 GiB. Check an archive's size (in bytes) before adding it, and keep the total under about 70 GiB:

```bash
curl -sI https://s3.ds4eng.condenser.arc.ucl.ac.uk/britishlibrary/1810_1819.zip | grep -i content-length
```

Running the playbook again skips any zip that is already in the bucket.

## Using the store from code

Any S3 client works. Use these settings:

- **Endpoint:** `https://<username>-s3.comp0235.condenser.arc.ucl.ac.uk`
- **Access key:** `administrator`
- **Secret key:** the contents of `.versitypass`
- **Region:** `us-east-1`
- **Addressing:** path-style

For example, with the Python `minio` library from the object store exercises:

```python
from minio import Minio

client = Minio("<username>-s3.comp0235.condenser.arc.ucl.ac.uk",
    access_key="administrator",
    secret_key="<contents of .versitypass>"
)

for obj in client.list_objects("britishlibrary"):
    print(obj.object_name, obj.size)
```

## Troubleshooting

- **The "Install quality of life tools" task fails on the `ansible` package.** Some AlmaLinux builds don't provide it. Replace `ansible` with `ansible-core` in `roles/common/tasks/tools.yaml`, then run `full.yaml` again.
- **The Web UI sign-in shows a network error.** Check that the S3 API endpoint on the sign-in page is your `-s3` address, not an IP address.
- **`terraform apply` restarted the VM.** Any change to the VM resource restarts it, because `restart_after_update = true`. The gateway starts again on boot, and your data on `/data` is kept.

## Tear down

Run this with the same `-var` options as before, unless you used `terraform.tfvars`:

```bash
terraform destroy
```

This deletes the VM **and its data disk**, including everything in your buckets. Download anything you want to keep first.
