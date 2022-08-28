#!/bin/bash -eu

sudo yum install -y yum-plugin-kernel-livepatch
sudo yum kernel-livepatch enable -y

sudo yum update kpatch-runtime
sudo systemctl enable kpatch.service
sudo amazon-linux-extras enable livepatch
