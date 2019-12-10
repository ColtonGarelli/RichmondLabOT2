from opentrons import protocol_api
import opentrons
metadata = {
    'protocolName': 'My Protocol',
    'author': 'Name <email@address.com>',
    'description': 'Simple protocol to get started using OT2',
    'apiLevel': '2.0',
}


def run(protocol: protocol_api.ProtocolContext):
    # plate = protocol.load_labware('p300_multi', 'left')
    opentrons.robot.update_config(name='Huey')
    plate = protocol.load_labware('corning_96_wellplate_360ul_flat', '4')
    tiprack300_1 = protocol.load_labware('opentrons_96_tiprack_300ul', '10')
    p300 = protocol.load_instrument('p300_multi', 'left', tip_racks=[tiprack300_1])
    p300.pick_up_tip()
    p300.aspirate(50, plate.well('A1'))
    p300.dispense(50, plate.well('A1'))
