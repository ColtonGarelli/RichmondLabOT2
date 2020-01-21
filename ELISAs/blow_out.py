from opentrons import protocol_api
from opentrons.protocol_api.contexts import Labware, InstrumentContext

metadata = {'apiLevel': '2.0'}


def setup_wash(protocol: protocol_api.ProtocolContext):
    plate = protocol.load_labware('corning_96_wellplate_360ul_flat', '7')
    tiprack300_1 = protocol.load_labware('opentrons_96_tiprack_300ul', '10')
    # tiprack300_2 = protocol.load_labware('opentrons_96_tiprack_300ul', '10')

    reservoir = [protocol.load_labware('nest_12_reservoir_15ml', '8'),
                 protocol.load_labware('nest_12_reservoir_15ml', '3')]
    p300m = protocol.load_instrument('p300_multi', 'left', tip_racks=[tiprack300_1])
    return p300m


def run(protocol: protocol_api.ProtocolContext):
    p300m = setup_wash(protocol)

    p300m.