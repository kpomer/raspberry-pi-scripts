# Raspberry Pi Time Machine Server Step-By-Step Instructions

#### Attach SSD to Raspberry Pi

#### Format the entire SSD with the Linux 'ext4' filesystem. This erases all data. Make sure to confirm the drive is in the /dev/sda location first!

```bash
sudo mkfs.ext4 /dev/sda
```

#### Create a directory that will act as a mount point for the SSD.

```bash
sudo mkdir -p /mnt/timemachine
```

#### Mount the SSD to the newly created directory. The drive is now accessible.

```bash
sudo mount /dev/sda /mnt/timemachine
```

#### Add a line to /etc/fstab to automatically mount the SSD on every boot.

```bash
echo '/dev/sda /mnt/timemachine ext4 defaults 0 0' | sudo tee -a /etc/fstab
```

#### Mount all filesystems listed in /etc/fstab that aren't already mounted.

```bash
sudo mount -a
```

#### Update the package list.

```bash
sudo apt update
```

#### Install Samba for file sharing and Avahi for network discovery.

```bash
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

#### (Optional) Create subdirectories on the SSD for each MacBook's backups.

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
 	fruit:time machine max size = 2T #(Optional) Set Max Size
 	fruit:time machine = yes

[Macbook2]
 	path = /mnt/timemachine/Macbook2
 	read only = No
 	valid users = timemachine
 	fruit:time machine max size = 2T #(Optional) Set Max Size
 	fruit:time machine = yes
```

#### Update package lists again.

```bash
sudo apt update
```

#### Install a command-line tool to test the Samba shares.

```bash
sudo apt install smbclient -y
```

#### List the Samba shares available on the local machine for the 'timemachine' user.

```bash
smbclient -L localhost -U timemachine
```

## The next steps are performed on the Macbooks

#### Open Time Machine and add a new backup device

#### Select the newly visible drive specific to that macbook

#### After choosing to backup, you must enter the new timemachine username and password from the raspberry pi setup

#### Start your backup!
