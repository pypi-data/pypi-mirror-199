from AoE2ScenarioParser.datasets.player_data import Player
from AoE2ScenarioParser.datasets.trigger_data import PanelLocation
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.local_config import folder_de
from AoE2ScenarioParser.scenarios.aoe2_scenario import AoE2Scenario

filename = "aassdd"
scenario = AoE2Scenario.from_file(f"{folder_de}{filename}.aoe2scenario")
tm, um, mm, xm, pm, msm = scenario.trigger_manager, scenario.unit_manager, scenario.map_manager, scenario.xs_manager, \
                     scenario.player_manager, scenario.message_manager

test = tm.add_trigger("test")
test.new_effect.display_instructions(
    object_list_unit_id=UnitInfo.PALADIN.ID,
    source_player=Player.ONE,
    display_time=10,
    instruction_panel_position=PanelLocation.CENTER,
)

scenario.write_to_file(f"{folder_de}{filename}_written.aoe2scenario")
