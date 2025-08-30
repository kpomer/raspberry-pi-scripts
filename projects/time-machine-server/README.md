# Raspberry Pi Time Machine Server Step-By-Step Instructions

## Preparation and External Drive Identification

#### Attach drive to Raspberry Pi and use the following command to identify it by the size

```bash
lsblk
```

#### Determine the Device Path by running the following command

```bash
sudo blkid
```

- For instructions we will use the sample path `/dev/sdX`, but for your own setup **make sure to use your actual path**:

---

## Drive Format and Mounting

#### Format the entire drive with the Linux 'ext4' filesystem. This erases all data.

- Replace `/dev/sdX` with your actual device path

```bash
sudo mkfs.ext4 /dev/sdX
```

#### Create a directory that will act as a mount point for the drive.

```bash
sudo mkdir -p /mnt/timemachine
```

#### Mount the drive temporarily using the device path

- Replace `/dev/sdX` with your actual device path

```bash
sudo mount /dev/sdX /mnt/timemachine
```

#### Get the UUID of your drive and store the value for later

- Replace `/dev/sdX` with your actual device path

```bash
sudo blkid /dev/sdX
```

- For instructions we will use the sample value of `UUID="1111a222-3333-4bbb-555c-6666d7777eee"`, but for your own setup **make sure to use your actual UUID**:

#### Add a line to /etc/fstab to automatically mount the drive on every boot using the UUID

- Replace with your actual UUID value

```bash
echo 'UUID=1111a222-3333-4bbb-555c-6666d7777eee  /mnt/timemachine  ext4  defaults  0  2' | sudo tee -a /etc/fstab
```

#### Mount all filesystems listed in /etc/fstab that aren't already mounted. This should have no output if everything is setup correctly

```bash
sudo mount -a
```

#### Confirm that the drive is mounted. This will show your TARGET mount point with the drive UUID as the SOURCE

```bash
findmnt /mnt/timemachine
```

---

## Update Raspberry Pi and Install Software

#### Update the package list and install Samba for file sharing and Avahi for network discovery.

```bash
sudo apt update
sudo apt install samba samba-common avahi-daemon -y
```

#### Enable and start the Samba service for file sharing.

```bash
sudo systemctl enable smbd
sudo systemctl start smbd
```

#### Enable and start the Avahi service to make the server discoverable on the network.

```bash
sudo systemctl enable avahi-daemon
sudo systemctl start avahi-daemon
```

#### Create a new system user for Time Machine backups.

```bash
sudo adduser timemachine
```

#### Set a Samba password for the 'timemachine' user.

```bash
sudo smbpasswd -a timemachine
```

#### (Optional) Create subdirectories on the drive for each MacBook's backups.

```bash
sudo mkdir -p /mnt/timemachine/Macbook1
sudo mkdir -p /mnt/timemachine/Macbook2
```

#### Change ownership of the backup directories to the 'timemachine' user.

```bash
sudo chown -R timemachine:timemachine /mnt/timemachine/*
```

#### Open the Samba configuration file for editing.

```bash
sudo nano /etc/samba/smb.conf
```

#### Add the following configuration

- Note `fruit:time machine max size` is optional to set size limits if preferred. Make sure these are correct for your specific drive size

```bash
### These lines are added within the [global] section to enable Time Machine compatibility.
fruit:model = MacSamba
idmap config * : backend = tdb
vfs objects = catia fruit streams_xattr

### These are separate sections added below to define the shares for each MacBook, including the maximum allowed size for each
[Macbook1]
 	path = /mnt/timemachine/Macbook1
 	read only = No
 	valid users = timemachine
	# (Optional) Set maximum backup size
 	fruit:time machine max size = 2T
 	fruit:time machine = yes

[Macbook2]
 	path = /mnt/timemachine/Macbook2
 	read only = No
 	valid users = timemachine
	# (Optional) Set maximum backup size
 	fruit:time machine max size = 2T
 	fruit:time machine = yes
```

#### Install a command-line tool to test the Samba shares.

```bash
sudo apt install smbclient -y
```

#### List the Samba shares available on the local machine for the 'timemachine' user.

```bash
smbclient -L localhost -U timemachine
```

## Configure Time Machine on Macbooks

#### Open Time Machine and add a new backup device

#### Select the newly visible drive specific to that macbook

- If the drive does not automatically appear, connect manually via Finder using `Go → Connect to Server → smb://<raspberrypi-hostname>/Macbook1`

#### After choosing to backup, you must enter the new timemachine username and password from the raspberry pi setup

#### Start your backup!

## Future Monitoring

#### View the amount of time machine storage being used for each machine

```bash
sudo du -sh /mnt/timemachine/*
```

#### Check Samba logs for troubleshooting

```bash
sudo tail -f /var/log/samba/log.smbd
```
