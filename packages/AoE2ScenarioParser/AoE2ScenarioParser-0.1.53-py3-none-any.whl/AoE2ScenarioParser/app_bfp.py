from AoE2ScenarioParser.local_config import folder_de
from AoE2ScenarioParser.scenarios.aoe2_scenario import AoE2Scenario
from AoE2ScenarioParser.sections.aoe2_file_section import SectionName

filename = "newww"
scenario = AoE2Scenario.from_file_bfp(f"{folder_de}{filename}.aoe2scenario")

# scenario = AoE2Scenario.from_file(f"{folder_de}{filename}.aoe2scenario")
# print(scenario.sections[SectionName.FILE_HEADER.value])
