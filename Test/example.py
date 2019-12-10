from opentrons import protocol_api
import opentrons.protocol_api.labware as labware

metadata = {'apiLevel': '2.0',
            'protocolName': 'Ex2'}


#
# elisa_plate_name = 'NUNC-MaxiSorp-ELISA-96'.lower()

# if elisa_plate_name not in list(labware):
# elisa_plate = labware.(elisa_plate_name,
#                                 grid=(12, 8),
#                                 spacing=(9, 9),
#                                 diameter=7,
#                                 depth=11.3,
#                                 volume=350)


def run(protocol: protocol_api.ProtocolContext):

    plate = protocol.load_labware('corning_96_wellplate_360ul_flat', '4')
    tiprack_1 = protocol.load_labware('opentrons_96_tiprack_300ul', '10')

    p300 = protocol.load_instrument('p300_multi', 'left', tip_racks=[tiprack_1])

    # p300.transfer(100, plate.columns(0), plate.columns(1))
    p300.pick_up_tip()
    p300.aspirate(100, plate['A1'])
    p300.dispense(100, plate['A2'])
    p300.return_tip()

