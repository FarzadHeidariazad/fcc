from database import Database
from database import TabelMaken
from functions import Lijstnamen_Maken
from functions import lijstnamen_gebruiken

# Initialisatie:
Database.initialise(host = 'localhost',database = 'djangodb-8April-1000.dump',user = 'postgres',password = 'postgres')
TabelMaken('runbook_converter_addrip','converter_addrip')
TabelMaken('runbook_converter_addrgrp','converter_addrgrp')
TabelMaken('runbook_converter_policy','converter_policy')
TabelMaken('runbook_converter_servgrp','converter_servgrp')
TabelMaken('runbook_converter_servother','converter_servother')
TabelMaken('runbook_converter_servtcpudp','converter_servtcpudp')

# gebruikersinvoer:
Subnet_van_VLAN = '10.128.109.0/24'
Conversion_ID_from_Converter = '9'

# tabellen vullen
Lijstnamen,LijstServ = Lijstnamen_Maken(Subnet_van_VLAN,Conversion_ID_from_Converter)
runbook_addrip,runbook_addrgr,runbook_Cpolic = lijstnamen_gebruiken(Lijstnamen,LijstServ,Conversion_ID_from_Converter)
