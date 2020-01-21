from opentrons import protocol_api
from opentrons.protocol_api.contexts import Labware, InstrumentContext, ProtocolContext
import csv
import typing
metadata = {'apiLevel': '2.0'}


def setup_50(protocol: protocol_api.ProtocolContext):
    # TODO: figure out how to run with incomplete plates
    plates = [protocol.load_labware('biorad_96_wellplate_200ul_pcr', '6')]
              # protocol.load_labware('corning_96_wellplate_360ul_flat', '8'),
              # protocol.load_labware('corning_96_wellplate_360ul_flat', '9')]

    # Should probably instantiate 3 racks
    tipracks_300 = [protocol.load_labware('opentrons_96_tiprack_300ul', '11')]
                    # protocol.load_labware('opentrons_96_tiprack_300ul', '11'),
                    # protocol.load_labware('opentrons_96_tiprack_300ul', '1'),
                    # protocol.load_labware('opentrons_96_tiprack_300ul', '2'),
                    # protocol.load_labware('opentrons_96_tiprack_300ul', '3')]
    # FACS buffer
    # facs = protocol.load_labware('nest_12_reservoir_15ml', '9')
    facs = protocol.load_labware("usascientific_12_reservoir_22ml", 4)
    p50s = protocol.load_instrument('p50_single', 'right', tip_racks=tipracks_300)
    tuberack = protocol.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', '7')
    return p50s, plates, tuberack, tipracks_300, facs


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


def distribute_mm_to_map(p50s: InstrumentContext, plates: [Labware],
                         tuberack: Labware, protocol: protocol_api.ProtocolContext,
                         groups: typing.Generator, platemap: list):

    tubes = tuberack.wells()[:6]
    # next(groups)
    for i in range(len(plates)):
        current_plate = plates[i]
        if i > len(plates)/2:
            p50s.well_bottom_clearance.aspirate = .8
        else:
            p50s.well_bottom_clearance.aspirate = 1
        for tube in tubes:
            current_group = next(groups)

            map_row_counter = 0
            p50s.pick_up_tip()
            for row in current_plate.rows():
                map_row = platemap[map_row_counter]
                for i in range(12):
                    if map_row[i] == current_group and map_row[i] != '':
                        # p50s.well_bottom_clearance.aspirate = .2
                        p50s.aspirate(volume=19, location=tube)
                        # p50s.well_bottom_clearance.dispense = 8
                        p50s.dispense(volume=19, location=row[i])
                    else:
                        pass
                map_row_counter += 1
            p50s.drop_tip()
        protocol.pause("Remove plate and press Resume to continue")


def run(protocol:ProtocolContext):
    p50s, plates, tuberack, tiprack300_1, facs = setup_50(protocol)
    # Enter the appropriate map file path
    platemap = load_platemap('/data/platemaps/qPCR/010619-morphea-qpcr-for-revisions.csv')
    # platemap = load_platemap('/Users/coltongarelli/pyLibraries/RichmondOT2/010619-morphea-qpcr-for-revisions.csv')
    groups = get_groups(platemap)

    distribute_mm_to_map(p50s=p50s, plates=plates, tuberack=tuberack,
                         platemap=platemap, groups=groups, protocol=protocol)

