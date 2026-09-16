# Microduck seed image

This rootfs was built from Armbian Minimal + scripts from the local
`pollen-robotics/microduck` clone (see `/opt/microduck`).

Bring-up (same as upstream `docs/robot/install-dev.md`):

    sudo sh /opt/microduck/scripts/provision.sh

Or fill `/boot/microduck.env` from `/boot/microduck.env.example` and:

    sudo systemctl enable --now microduck-firstboot

Not an official Pollen factory image. Releases stay signature-verified via `updaterd`.
