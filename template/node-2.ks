#version=DEVEL
# Firewall configuration
firewall --disabled
# Install OS instead of upgrade
install
# Use CDROM installation media
url --url=$tree
# Root password
rootpw --iscrypted $1$78888O7t$XAdzFmSUXy7Ysqayh7IU/1
# System authorization information
auth  --useshadow  --passalgo=sha512
# Use graphical install
#graphical
# System keyboard
keyboard us
# System language
lang en_US
# SELinux configuration
selinux --disabled
# Do not configure the X Window System
skipx
# Installation logging level
logging --level=info
# Reboot after installation
reboot
# Network information

# System timezone
timezone --utc Asia/Shanghai
# System bootloader configuration
bootloader --location=mbr
# Clear the Master Boot Record
zerombr
# Partition clearing information
clearpart --all --initlabel 
ignoredisk --only-use=sda

# Disk partitioning information
part / --asprimary --fstype="ext4" --grow --size=1
part /boot --asprimary --fstype="ext4" --size=500
#part swap --asprimary --fstype="swap" --size=4096
%packages --ignoremissing
@^minimal
@core
kexec-tools
vim-minimal
wget 
git
net-tools
%end
%post --interpreter=/usr/bin/bash
touch /opt/install.txt
echo "1" > /var/log/install.txt
$SNIPPET("log_ks_post_nochroot")
$SNIPPET("post_anamon")
$SNIPPET("log_ks_post")
$SNIPPET("post_install_network_config")
$yum_config_stanza
%end
%addon com_redhat_kdump --enable --reserve-mb=auto
%end
%pre --interpreter=/usr/bin/bash
touch /opt/install
$SNIPPET("log_ks_pre")
$SNIPPET("kickstart_start")
$SNIPPET("pre_install_network_config")
echo "start pre install ">> /root/install.txt
# Enable installation monitoring
$SNIPPET("pre_anamon")
$SNIPPET("network_config")
$SNIPPET("kickstart_done")
%end

