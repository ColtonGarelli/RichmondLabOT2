from opentrons import protocol_api
from opentrons.protocol_api.contexts import Labware, InstrumentContext


def setup_wash(protocol: protocol_api.ProtocolContext):
    plate = protocol.load_labware('corning_96_wellplate_360ul_flat', '1')
    tiprack300_1 = protocol.load_labware('opentrons_96_tiprack_300ul', '10')
    reservoir = [protocol.load_labware('nest_12_reservoir_15ml', '2'),
                 protocol.load_labware('nest_12_reservoir_15ml', '3')]

    p300 = protocol.load_instrument('p300_multi', 'left', tip_racks=[tiprack300_1])
    return p300, reservoir, plate




def run(protocol: protocol_api.ProtocolContext):

    p300, reservoir, plate = setup_wash(protocol)
    p300.blow_out(p300.trash_container.wells()[0])
    p300.blow_out(p300.trash_container.wells()[0])
    p300.blow_out(p300.trash_container.wells()[0])
    p300.blow_out(p300.trash_container.wells()[0])
    p300.blow_out(p300.trash_container.wells()[0])
    p300.blow_out(p300.trash_container.wells()[0])

