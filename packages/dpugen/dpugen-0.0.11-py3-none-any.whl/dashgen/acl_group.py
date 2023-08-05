#!/usr/bin/python3

import os
import sys
from copy import deepcopy

from dpugen.confbase import ConfBase
from dpugen.confutils import common_main


class AclGroups(ConfBase):

    def __init__(self, params={}):
        super().__init__(params)
        self.num_yields = 0

    def items(self):
        print('  Generating %s ...' % os.path.basename(__file__), file=sys.stderr)
        p = self.params
        cp = self.cooked_params
        IP_STEP1 = cp.IP_STEP1
        IP_STEP_ACL = cp.IP_STEP_ACL
        IP_STEP_NSG = cp.IP_STEP_NSG
        IP_STEP_ENI = cp.IP_STEP_ENI
        IP_STEPE = cp.IP_STEPE
        IP_R_START = cp.IP_R_START
        IP_L_START = cp.IP_L_START
        ACL_NSG_COUNT = p.ACL_NSG_COUNT
        ACL_RULES_NSG = p.ACL_RULES_NSG
        IP_PER_ACL_RULE = p.IP_PER_ACL_RULE

        for eni_index in range(1, p.ENI_COUNT + 1):
            local_ip = IP_L_START + (eni_index - 1) * IP_STEP_ENI
            l_ip_ac = deepcopy(str(local_ip)+"/32")

            for table_index in range(1, (ACL_NSG_COUNT*2+1)):
                table_id = eni_index * 1000 + table_index

                rules = []
                rappend = rules.append
                for ip_index in range(1, (ACL_RULES_NSG+1), 2):
                    remote_ip_a = IP_R_START + (eni_index - 1) * IP_STEP_ENI + (
                        table_index - 1) * IP_STEP_NSG + (ip_index - 1) * IP_STEP_ACL

                    ip_list_a = [str(remote_ip_a + expanded_index * IP_STEPE) +
                                 "/32" for expanded_index in range(0, IP_PER_ACL_RULE)]
                    ip_list_a.append(l_ip_ac)

                    rule_a = {
                        "priority": ip_index,
                        "action": "allow",
                        "terminating": False,
                        "src_addrs": ip_list_a[:],
                        "dst_addrs":  ip_list_a[:],
                    }
                    rappend(rule_a)
                    remote_ip_d = remote_ip_a + IP_STEP1

                    ip_list_d = [str(remote_ip_d + expanded_index * IP_STEPE) +
                                 "/32" for expanded_index in range(0, IP_PER_ACL_RULE)]
                    ip_list_d.append(l_ip_ac)

                    rule_d = {
                        "priority": ip_index+1,
                        "action": "deny",
                        "terminating": True,
                        "src_addrs": ip_list_d[:],
                        "dst_addrs":  ip_list_d[:],
                    }
                    rappend(rule_d)

                # add as last rule in last table from ingress and egress an allow rule for all the ip's from egress and ingress
                if ((table_index - 1) % 3) == 2:
                    all_ipsA = IP_R_START + (eni_index - 1) * IP_STEP_ENI + (table_index % 6) * IP_STEP_NSG
                    all_ipsB = all_ipsA + 1 * IP_STEP_NSG
                    all_ipsC = all_ipsA + 2 * IP_STEP_NSG

                    ip_list_all = [
                        l_ip_ac,
                        str(all_ipsA)+"/14",
                        str(all_ipsB)+"/14",
                        str(all_ipsC)+"/14",
                    ]

                    rule_allow_all = {
                        "priority": ip_index+2,
                        "action": "allow",
                        "terminating": "true",
                        "src_addrs": ip_list_all[:],
                        "dst_addrs":  ip_list_all[:],
                    }
                    rappend(rule_allow_all)

                acl_group = deepcopy(
                    {
                        "ACL-GROUP:ENI:%d:TABLE:%d" % (eni_index, table_id): {
                            "acl-group-id": "acl-group-%d" % table_id,
                            "ip_version": "IPv4",
                            "rules": rules
                        }
                    }
                )
                self.num_yields += 1
                yield acl_group


if __name__ == "__main__":
    conf = AclGroups()
    common_main(conf)
