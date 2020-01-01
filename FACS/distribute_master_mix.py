from opentrons import protocol_api
from opentrons.protocol_api.contexts import Labware, InstrumentContext, ProtocolContext
import itertools
metadata = {'apiLevel': '2.0'}


def setup(protocol: protocol_api.ProtocolContext):
    # TODO: figure out how to run with incomplete plates
    plates = [protocol.load_labware('corning_96_wellplate_360ul_flat', '7'),
              protocol.load_labware('corning_96_wellplate_360ul_flat', '8'),
              protocol.load_labware('corning_96_wellplate_360ul_flat', '9')]

    # Should probably instantiate 3 racks
    tiprack300_1 = [protocol.load_labware('opentrons_96_tiprack_300ul', '10'),
                    protocol.load_labware('opentrons_96_tiprack_300ul', '11'),
                    protocol.load_labware('opentrons_96_tiprack_300ul', '1'),
                    protocol.load_labware('opentrons_96_tiprack_300ul', '2'),
                    protocol.load_labware('opentrons_96_tiprack_300ul', '3')]
    p300m = protocol.load_instrument('p300_multi', 'left', tip_racks=tiprack300_1)
    tuberack = protocol.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', '6')
    return p300m, plates, tuberack, tiprack300_1

def next_tip(tipracks: [Labware], tip_count: int):
    rack_counter = -1
    if rack_counter != tip_count // 96:
        rack_counter = tip_count // 96
        tip_list = reversed(tipracks[rack_counter].wells())
    for tip in tip_list:
        yield tip


def distribute_master_mix(p300m: InstrumentContext, plates: [Labware],
                          tuberack: Labware, tipracks: [Labware]):
    tubes = tuberack.wells()[0:4]
    p300m.well_bottom_clearance.dispense = .02
    tip_counter = 0
    # to_remove is the number of wells to be removed from the final row. all prior rows will be assumed to be filled
    to_remove = 11
    to_remove = 12 - to_remove
    # last_row is the index of the last row (rows() returns 2D list of rows by well)
    last_row = 1
    plate = plates[0]
    # for plate in plates:
    wells = plate.rows()[:2]
    wells[last_row] = wells[last_row][:to_remove]
    # for example, pop the last 8 in a row for a
    # for plate in plates:
    #     # last_row is the index of the last row (rows() returns 2D list of rows by well)
    #
    #     plate = plates[0]
    #     # for plate in plates:
    #     wells = plate.rows()[:2]
    #     wells[last_row] = wells[last_row][:to_remove]
    group_counter = 0
    for tube in tubes:
        p300m.well_bottom_clearance.aspirate = .1
        print(wells)
        wells = plate.rows()[:2+group_counter]
        group_counter += 2
        wells[last_row] = wells[last_row][:to_remove]
        for row in wells:
            for well in row:
                p300m.pick_up_tip(location=next(next_tip(tipracks=tipracks, tip_count=tip_counter)), presses=2, increment=.05)
                print(tube, well)
                p300m.aspirate(volume=100, location=tube)
                p300m.dispense(volume=100, location=well)
                p300m.well_bottom_clearance.aspirate = .02
                p300m.mix(volume=60, repetitions=3, location=well)
                p300m.drop_tip()
                tip_counter += 1

    # 1D Labware.wells() returns 1D list of wells

def run(protocool:ProtocolContext):
    p300m, plates, tuberack, tiprack300_1 = setup(protocool)
    distribute_master_mix(p300m=p300m, plates=plates, tuberack=tuberack, tipracks=tiprack300_1)