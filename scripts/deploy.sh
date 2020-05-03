#! /bin/bash

INSTANCE='ec2-18-236-86-253.us-west-2.compute.amazonaws.com'

rsync --delete -a -e "ssh -i ~/.ssh/api_tlb.pem" . ubuntu@$INSTANCE:~/api/
