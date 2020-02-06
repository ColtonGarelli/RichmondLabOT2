from opentrons import protocol_api
from opentrons.protocol_api.contexts import Labware, InstrumentContext, ProtocolContext
import csv, typing
from opentrons.drivers.rpi_drivers import gpio
metadata = {'apiLevel': '2.0'}


def setup_300(protocol: protocol_api.ProtocolContext):
    # TODO: figure out how to run with incomplete plates
    plates = [protocol.load_labware('corning_96_wellplate_360ul_flat', '8'),
              protocol.load_labware('corning_96_wellplate_360ul_flat', '8'),
              protocol.load_labware('corning_96_wellplate_360ul_flat', '9')]

    # Should probably instantiate 3 racks
    tiprack300_1 = [protocol.load_labware('opentrons_96_tiprack_300ul', '10'),
                    protocol.load_labware('opentrons_96_tiprack_300ul', '11'),
                    protocol.load_labware('opentrons_96_tiprack_300ul', '1'),
                    protocol.load_labware('opentrons_96_tiprack_300ul', '2'),
                    protocol.load_labware('opentrons_96_tiprack_300ul', '3')]
    p300m = protocol.load_instrument('p300_multi', 'left', tip_racks=tiprack300_1)
    tuberack = protocol.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', '7')
    return p300m, plates, tuberack, tiprack300_1


def setup_50(protocol: protocol_api.ProtocolContext):
    # TODO: figure out how to run with incomplete plates
    plates = [protocol.load_labware('corning_96_wellplate_360ul_flat', '8')]
              # protocol.load_labware('corning_96_wellplate_360ul_flat', '8'),
              # protocol.load_labware('corning_96_wellplate_360ul_flat', '9')]

    # Should probably instantiate 3 racks
    tipracks_300 = [protocol.load_labware('opentrons_96_tiprack_300ul', '11')]
                    # protocol.load_labware('opentrons_96_tiprack_300ul', '11'),
                    # protocol.load_labware('opentrons_96_tiprack_300ul', '1'),
                    # protocol.load_labware('opentrons_96_tiprack_300ul', '2'),
                    # protocol.load_labware('opentrons_96_tiprack_300ul', '3')]
    # FACS buffer
    facs = protocol.load_labware('nest_12_reservoir_15ml', '9')
    # facs = protocol.load_labware("usascientific_12_reservoir_22ml", 4)
    p50s = protocol.load_instrument('p50_single', 'left', tip_racks=tipracks_300)

    tuberack = protocol.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', '7')
    return p50s, plates, tuberack, tipracks_300, facs


def next_tip(tipracks: [Labware], rack: int):
    tip_list = reversed(tipracks[rack-1].wells())
    return tip_list


def distribute_master_mix_p50(p50s: InstrumentContext, plates: [Labware],
                              tuberack: Labware, tipracks: [Labware], facs: Labware):
    tubes = tuberack.wells()[:2]
    # to_remove is the number of wells to be removed from the final row. all prior rows will be assumed to be filled
    to_remove = 6
    to_remove = 12 - to_remove
    p50s.well_bottom_clearance.dispense = 10
    p50s.well_bottom_clearance.aspirate = 3
    # last_row is the index of the last row (rows() returns 2D list of rows by well)
    for plate in plates:
        start_row = 0
        num_rows = 2
        # first group @ row 0 (row A)
        last_row = num_rows
        for tube in tubes:
            group = plate.rows()[start_row: last_row]
            last_group = group[num_rows-1][:to_remove]
            group[num_rows-1] = last_group
            p50s.pick_up_tip()
            p50s.transfer(volume=50, source=tube, dest=group,
                          new_tip='never',)  # comment out for actual runs. this is for test
            p50s.drop_tip()
            p50s.pick_up_tip()
            p50s.transfer(volume=50, source=facs['A1'], dest=group,
                          new_tip='never')  # comment out for actual runs. this is for test
            p50s.drop_tip()
            start_row += num_rows
            last_row += num_rows


def distribute_mm_to_map(p50s: InstrumentContext, plates: [Labware],
                         tuberack: Labware, tipracks: [Labware], facs: Labware,
                         groups: typing.Generator, platemap: list, protocol: protocol_api.ProtocolContext):

    tubes = tuberack.wells()[:3]
    plate = plates[0]
    next(groups)
    # for plate in plates:
    for tube in tubes:
        current_group = next(groups)
        map_row_counter = 0
        p50s.pick_up_tip()
        for row in plate.rows():
            map_row = platemap[map_row_counter]
            for i in range(12):
                if map_row[i] == current_group and map_row[i] != '':
                    p50s.well_bottom_clearance.aspirate = 10
                    p50s.aspirate(volume=50, location=tube)
                    p50s.well_bottom_clearance.dispense = 10
                    p50s.dispense(volume=50, location=row[i])
                else:
                    pass
            map_row_counter += 1
        p50s.drop_tip()


def button_pause(protocol: protocol_api.ProtocolContext):
    if gpio.read(gpio.INPUT_PINS['BUTTON_INPUT']):
        protocol.reset()


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
    tip_gen = next_tip(p300m.tip_racks, 1)
    for tube in tubes:
        p300m.well_bottom_clearance.aspirate = .1
        print(wells)
        wells = plate.rows()[:2+group_counter]
        group_counter += 2
        wells[last_row] = wells[last_row][:to_remove]
        for row in wells:
            for well in row:
                tip = next(tip_gen)
                print(tip)
                p300m.pick_up_tip(location=tip, presses=2, increment=.05)
                print(tube, well)
                p300m.aspirate(volume=100, location=tube)
                p300m.dispense(volume=100, location=well)
                p300m.well_bottom_clearance.aspirate = .02
                p300m.mix(volume=60, repetitions=3, location=well)
                p300m.drop_tip()
                tip_counter += 1

    # 1D Labware.wells() returns 1D list of wells


def get_groups(platemap: [[]]):
    groups = list()
    for row in platemap:
        for item in row:
            if item not in groups:
                groups.append(item)
            else:
                pass
    groups.sort()
    for i in groups:
        yield i


def load_platemap(file_path):
    with open(file_path, 'r+') as f:
        reader = csv.reader(f)
        next(reader)
        wells = list()
        for i in reader:
            wells.append(i)
        for i in wells:
            i.pop(0)
    return wells


def run(protocol:ProtocolContext):
    p50s, plates, tuberack, tiprack300_1, facs = setup_50(protocol)
    platemap = load_platemap('/data/platemaps/FACS/test.csv')
    # platemap = load_platemap('/Users/coltongarelli/PycharmProjects/PlateMapper/test.csv')
    groups = get_groups(platemap)

    distribute_mm_to_map(p50s=p50s, plates=plates, tuberack=tuberack, tipracks=tiprack300_1,
                         facs=facs, platemap=platemap, groups=groups, protocol=protocol)
