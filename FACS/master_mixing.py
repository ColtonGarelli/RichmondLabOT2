from opentrons import protocol_api
from opentrons.protocol_api.contexts import Labware, InstrumentContext

metadata = {'apiLevel': '2.0'}

# 100, 125, 200, 250, 500uL antibody tubes
# only have specs for 2ml 1.5ml and 500uL

def setup(protocol: protocol_api.ProtocolContext):
    # TODO: figure out how to run with incomplete plates
    # Should probably instantiate 3 racks
    tiprack300_1 = [protocol.load_labware('opentrons_96_tiprack_300ul', '10')]
    tiprack10 = [protocol.load_labware('opentrons_96_tiprack_10ul', '11')]
    p50s = protocol.load_instrument('p50_single', 'left', tip_racks=tiprack300_1)
    p10s = protocol.load_instrument('p10_single', 'right', tip_racks=tiprack10)
    tuberack = protocol.load_labware('biolegendantibody_24_tuberack_500ul_mm', '4')
    return p50s, p10s, tuberack, tiprack10


def load_plate():
    pass


def f_minus_one():
    # FMOs
    pass

def wash_plate():
    pass


def calc_volumes(num_ab: int,  vol_per_test: float, num_samples: int, num_xtra):
    """

    Args:
        num_ab:
        num_samples:
        vol_per_test:

    Returns:

    """
    tot_ab = (num_ab * vol_per_test)
    tot_facs = (num_samples * 100) - (tot_ab)
    # TODO: calculate volume of ab and FACS buffer to add for MM
    pass


def make_master_mix(num_abs, vol_ab,
                    protocol: protocol_api.ProtocolContext,
                    p10s: InstrumentContext, p50s: InstrumentContext, tube_rack: Labware):
    # TODO: tube rack mapping
    # define tube rack with # of antibodies
    # add x amount of each antibody to eppendorf tube as determined by calc_volume
    # loop through tuberack # ab times
    # eppendorf tube will be defined as in location A1
    if vol_ab > 10:
        pipette = p50s
    elif vol_ab <= 10:
        pipette = p10s
    else:
        print('uh oh!')
        pass
    tubes = tube_rack.wells()[:num_abs]
    pipette.well_bottom_clearance.aspirate = 1
    pipette.well_bottom_clearance.dispense = 2.5
    pipette.pick_up_tip()
    for tube in tubes:

        pipette.aspirate(volume=vol_ab, location=tube)
        pipette.dispense(volume=vol_ab, location=tube_rack.wells()[-1],)
        pipette.mix(volume=10)
        pipette.blow_out(tube_rack.wells()[-1])

    pipette.drop_tip()

def run(protocol: protocol_api.ProtocolContext):
    p50s, p10s, tuberack, tiprack_10 = setup(protocol)
    vol_ab = 6

    make_master_mix(num_abs=23, vol_ab=vol_ab, protocol=protocol, p10s=p10s, p50s=p50s,
                        tube_rack=tuberack)
