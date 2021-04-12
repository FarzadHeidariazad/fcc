from typing import List, Any
from query import QueryNu
from database import save_to_table

def Lijstnamen_Maken(S,c):
    lijst_voor_zoek_name = []
    lijst_voor_zoek_serv = []
    zoek_converter_addrip = QueryNu.converter_addrip(IPRange=S, ConvertID=c)
    if len(zoek_converter_addrip) > 0:
        for i in zoek_converter_addrip:
            lijst_voor_zoek_name.append(i[2])
            lijst_voor_zoek_name = list(set(lijst_voor_zoek_name))
        if len(lijst_voor_zoek_name) > 0:
            for i in lijst_voor_zoek_name:
                zoek_converter_addrgrp = QueryNu.converter_addrgrp(addrip=i, ConvertID=c)
        if len(zoek_converter_addrgrp) > 0:
            for i in zoek_converter_addrgrp:
                lijst_voor_zoek_name.append(i[3])
                lijst_voor_zoek_name = list(set(lijst_voor_zoek_name))
    if len(lijst_voor_zoek_name) > 0:
        for i in lijst_voor_zoek_name:
            zoek_converter_policy = QueryNu.converter_policy(addripgrp=i, ConvertID=c)
        if len(zoek_converter_policy) > 0:
            for i in zoek_converter_policy:
                lijst_voor_zoek_name.append(i[25])
                lijst_voor_zoek_name.append(i[26])
                lijst_voor_zoek_serv.append(i[27])
    return sorted(list(set(lijst_voor_zoek_name))), sorted(list(set(lijst_voor_zoek_serv)))

def lijstnamen_gebruiken(LN,LS,c):
    if len(LN) == 0: return None
    LN_addrip: list[Any]
    LN_addrgr: list[Any]
    LN_Cpolic: list[Any]
    LN_addrip = []
    LN_addrgr = []
    LN_Cpolic = []
    for LN_l in LN:
        LN_addrip_i = QueryNu.converter_addrip_name(LN_l, c)
        for x in LN_addrip_i:
            LN_addrip.append(x)
    for xDB in LN_addrip:
        LN_addrip_voorDB = str(xDB).replace('None', 'null').replace('(', '').replace(')', '').replace('[', '').replace(']', '')
        save_to_table('runbook_converter_addrip', LN_addrip_voorDB)
    #
    for LN_l in LN:
        LN_addrgr_i = QueryNu.converter_addrgrp(LN_l, c)
        for y in LN_addrgr_i:
            if len(LN_addrgr_i) > 0:
                LN_addrgr.append(y)
    if len(LN_addrgr) > 0:
        for yDB in LN_addrgr:
            LN_addrgr_voorDB = str(yDB).replace('None', 'null').replace('(', '').replace(')', '').replace('[','').replace(']', '')
            save_to_table('runbook_converter_addrgrp', LN_addrgr_voorDB)
    #
    for LN_l in LN:
        LN_Cpolic_i = QueryNu.converter_policy(LN_l, c)
        for z in LN_Cpolic_i:
            if len(LN_Cpolic_i) > 0:
                LN_Cpolic.append(z)
    if len(LN_Cpolic) > 0:
        for zDB in LN_Cpolic:
            LN_Cpolic_voorDB = str(zDB).replace('None', 'null').replace('(', '').replace(')', '').replace('[','').replace(']', '')
            save_to_table('runbook_converter_policy', LN_Cpolic_voorDB)
    #
    return LN_addrip,LN_addrgr,LN_Cpolic