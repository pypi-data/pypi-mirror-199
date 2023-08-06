from AoE2ScenarioParser.local_config import folder_de
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario
from AoE2ScenarioParser.sections.aoe2_file_section import SectionName

filename = "148"
scenario = AoE2DEScenario.from_file(f"{folder_de}{filename}.aoe2scenario")
tm, um, mm, xm, pm, msm = scenario.trigger_manager, scenario.unit_manager, scenario.map_manager, scenario.xs_manager, \
                     scenario.player_manager, scenario.message_manager


print(tm)
print(scenario.sections[SectionName.FILES.value])
exit()

scenario.write_to_file(f"{folder_de}{filename}_written.aoe2scenario")
