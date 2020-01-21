from opentrons import protocol_api
from opentrons.protocol_api.contexts import Labware, InstrumentContext

metadata = {'apiLevel': '2.0'}

# 100, 125, 200, 250, 500uL antibody tubes
# only have specs for 2ml 1.5ml and 500uL

def setup(protocol: protocol_api.ProtocolContext):
    # TODO: figure out how to run with incomplete plates
    plates = protocol.load_labware('corning_96_wellplate_360ul_flat', '11')
    # tubes = protocol.load_labware()
    # Should probably instantiate 3 racks
    tiprack300_1 = protocol.load_labware('opentrons_96_tiprack_300ul', '10')
    reservoir = [protocol.load_labware('nest_12_reservoir_15ml', '9'),
                 protocol.load_labware('nest_12_reservoir_15ml', '3')]
    p300m = protocol.load_instrument('p300_multi', 'left', tip_racks=[tiprack300_1])


def calc_volumes(num_ab: int, num_samples: int, ab_vol: float or [float], vol_per_test):

    # assumes 1:200 (.5uL/test)
    tot_ab = (num_ab * 0.5)
    tot_facs = (num_samples * 100) - (tot_ab)
    # TODO: calculate volume of ab and FACS buffer to add for MM
    pass


def make_master_mix():
    # TODO: tube rack mapping
    # define tube rack with # of antibodies

    # add x amount of each antibody to eppendorf tube as determined by calc_volume
    # loop through tuberack # ab times
    # eppendorf tube will be defined as in location A1


    pass


def load_plate():
    pass


def f_minus_one():
    # FMOs
    pass

def wash_plate():
    pass