from AoE2ScenarioParser import settings
from AoE2ScenarioParser.datasets.player_data import Player, Color
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.local_config import folder_de
from AoE2ScenarioParser.scenarios.aoe2_scenario import AoE2Scenario

# filename = "chance-condition-test2"
# scenario = AoE2Scenario.from_file(f"{folder_de}{filename}.aoe2scenario")

filename = "chance-condition-test3"
scenario2 = AoE2DEScenario.from_file(f"{folder_de}{filename}.aoe2scenario")
scenario2 = AoE2DEScenario.from_file(f"{folder_de}{filename}.aoe2scenario")

scenario2._debug_byte_structure_to_file('debug.txt')

# scenario.write_to_file(f"{folder_de}{filename}_written.aoe2scenario")
