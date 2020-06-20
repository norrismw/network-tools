# AntiAmericanJobs.py
---
## Requirements:
This program requires the NetMiko library which can be found [here] (https://github.com/ktbyers/netmiko). The library can be installed using `pip3 install netmiko`.

## Usage:
`python3 FHC.py username@device option`

There are currently two options -- `count` and `clear`. You should only select one of these options.

The `username@device` argument is required. An IP address or a hostname can be used for `device`. The user will be prompted for the password for `username@device` when the program runs. Either `count` or `clear` should be specified. Not both at once. By default, the connection will be made to port `22` of `device`. You can change the port by editing the file.

#### count:
The `count` command will get the policy IDs and the status/hit counts for each policy. A CSV will be written to the directory from which the program was run and will be named based on the value of `device`. The first column is the policy ID and the second column is hit count. The policies are displayed in the same order as they are arranged on the firewall.

#### clear:
The `clear` command will clear the hit counters for all policies on the specified `device`.
