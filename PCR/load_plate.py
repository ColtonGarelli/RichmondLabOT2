from opentrons.protocol_api import ProtocolContext, InstrumentContext
from opentrons.protocol_api.contexts import Labware, Well


def setup(protocol: ProtocolContext):
    plate = protocol.load_labware('biorad_96_wellplate_200ul_pcr', '6')
    tiprack300_1 = protocol.load_labware('opentrons_96_tiprack_300ul', '10')
    p50s = protocol.load_instrument('p50_single', 'right', tip_racks=[tiprack300_1])
    tuberack = protocol.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', '9')
    return p50s, tuberack, plate


def load_plate(protocol: ProtocolContext,
               p50s: InstrumentContext,
               tuberack: Labware,
               plate):
    tube_well_count = 0
    plate_well_count = 0
    p50s.well_bottom_clearance.aspirate = .01
    for tube in range(4):
        p50s.pick_up_tip()
        p50s.distribute(volume=19, source=tuberack.wells()[tube],
                        dest=plate.rows()[plate_well_count: plate_well_count+2],
                        new_tip='never',)
        plate_well_count += 2
        p50s.drop_tip()


def run(protocol: ProtocolContext):
    load_plate(protocol, *setup(protocol=protocol))
