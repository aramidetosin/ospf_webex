import os
from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command, napalm_get
from nornir.plugins.functions.text import print_result
from rich import print
import requests
import json

nr = InitNornir()

def test(task):
    dev_name = task.host
    my_list = []
    result = task.run(netmiko_send_command, command_string='show ip ospf nei', use_genie=True)
    task.host["facts"] = result.result
    interfaces = task.host['facts']['interfaces']
    #
    for interface in interfaces:
        neighbor = interfaces[interface]['neighbors']
        for adj in neighbor:
            my_list.append(adj)
    num_nei = len(my_list)
    if num_nei == 1:
        print(f"{dev_name}: [green]PASSED[/green]")
    else:
        print(f"{dev_name}: [red]FAILED[/red]")
        failed_report(dev_name)

def failed_report(dev_name):
    header = {"Authorization": "Bearer xxx",
              "Content-Type": "application/json"}

    data = {"roomId": "xxx",
            "text": f"{dev_name} FAIL: OSPF NEIGHBOR FAILURE"}
    return requests.post("https://api.ciscospark.com/v1/messages", headers=header, data=json.dumps(data), verify=True)


result = nr.run(task=test)
# import pdb
# pdb.set_trace()
