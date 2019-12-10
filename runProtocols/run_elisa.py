from opentrons import protocol_api
from ELISAs import proteinuria_elisa, load_plate, wash_elisa
import errors
import opentrons

metadata = {'apiLevel': '2.0',
            'protocolName': 'Ex2'}


def setup_run(protocol: protocol_api.ProtocolContext):
    plate = protocol.load_labware('corning_96_wellplate_360ul_flat', '4')
    tiprack300_1 = protocol.load_labware('opentrons_96_tiprack_300ul', '10')
    p300 = protocol.load_instrument('p300_multi', 'left', tip_racks=[tiprack300_1])
    reservoir = protocol.load_labware('axygen_1_reservoir_90ml', '6')
    eppen_rack = protocol.load_labware('tuberack') # define and load tuberack
    return plate, tiprack300_1, reservoir, p300, eppen_rack


def run(protocol: protocol_api.ProtocolContext):
    plate, tiprack, rez, p300, eppendorfs = setup_run(protocol)
    checks = protocol.loaded_labwares.items()
    if len(checks) == 1:
        raise errors.LabwareNotLoadedException("Labware is not loaded into current protocol. "
                                               "Make sure you haven't instantiated two ProtocolContext instances")
    checks = protocol.loaded_instruments
    if len(checks) == 0:
        raise errors.LabwareNotLoadedException("Labware is not loaded into current protocol. "
                                               "Make sure you haven't instantiated two ProtocolContext instances")

    # load primary antibody
    # TODO: try to make this interactive?
    # wash plate
    wash_elisa.elisa_wash(protocol, p300m=p300, reservoir=rez, plate=plate,
                          num_washes=3, wash_volume=100)
    # add antibody to plate
    load_plate.add_samples(protocol, p300, rez, tuberack=eppendorfs)
    # load samples/standards
    # load samples

    # load standards
    # if plate not coated
    #
    # load antibody
    # wait an hour
    #
    # proteinuria_elisa.proteinuria(protocol)
