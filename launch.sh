#!/bin/bash

QEMU=qemu-system-arm
KERNEL=zImage-qemuarm.bin
ROOTFS=rpi-basic-image-qemuarm.ext3

$QEMU -kernel $KERNEL -net nic,vlan=0 -net tap,vlan=0,ifname=tap0,script=no,downscript=no \
-M versatilepb -hda $ROOTFS -no-reboot -show-cursor \
-usb -usbdevice wacom-tablet -no-reboot -m 128 \
--append "root=/dev/sda rw console=ttyAMA0,115200 console=tty ip=192.168.7.2::192.168.7.1:255.255.255.0 mem=128M highres=off "
