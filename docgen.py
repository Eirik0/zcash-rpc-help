#!/usr/bin/env python3

import datetime

from slickrpc import Proxy
from slickrpc.exc import RpcException

TIME_STARTED = datetime.datetime.now()

zcash_proxy = Proxy("http://%s:%s@127.0.0.1:%s" %
    (
        "rpcuser",
        "rpcpass",
        "8232")
    )

def call_rpc(name, args=[]):
    print("%s: ./zcash-cli %s %s" %
        (
            datetime.datetime.now() - TIME_STARTED,
            name, 
            ' '.join([str(arg) for arg in args]))
        )
    try:
        return zcash_proxy.__getattr__(name)(*args)
    except RpcException as e:
        print("RpcException: %s" % (e))
        return None

# Call "help" to generate a list of rpcs
help_rpc_output = call_rpc("help")
rpctype_to_rpcnames = dict() # Is this in order ?
rpcname_to_helptext = dict() # Is this in order ?
current_rpctype = None
for help_rpc_output_line in help_rpc_output.split("\n"):
    if help_rpc_output_line == "":
        continue
    elif help_rpc_output_line.startswith("=="):
        current_rpctype = help_rpc_output_line[3:-3]
        rpctype_to_rpcnames[current_rpctype] = []
    else:
        rpc_name = help_rpc_output_line.split()[0]
        rpctype_to_rpcnames[current_rpctype].append(rpc_name)

# Call "help <rpc>" for each rpc
for section in rpctype_to_rpcnames:
    for rpcname in rpctype_to_rpcnames[section]:
        rpcname_to_helptext[rpcname] = call_rpc("help", [rpcname])
