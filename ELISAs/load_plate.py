from opentrons.protocol_api import ProtocolContext
import opentrons
from opentrons.protocol_api.contexts import InstrumentContext, Labware
# TODO: delete after i figure out tuberack defintion and how to access specific locations

# **** Can use labware.rows['A'] and labware.columnss['1'][0] to access rows/cols
# tuberack = opentrons.labware.load('opentrons-tuberack-1.5ml-eppendorf', slot=)


def add_antibody(protocol: ProtocolContext,
                 p300_multi: InstrumentContext,
                 reservoir: Labware,
                 tuberack: Labware,
                 plate: Labware,
                 wells: [[]]):
    """

    Args:
        protocol:
        p300_multi:
        reservoir: hopefully we will get a 12 well trough
        tuberack:
        wells: a column-wise list of lists of wells in use

    Returns:
        Nothing as of now

    """

    #  move liquid from reservoir to plate with p300 multi
    for _ in wells:
        i = 0
        p300_multi.transfer(source=reservoir, dest=plate.columns()[i], new_tip='never')
        i += 1
    #  pause for 2 hours
    protocol.delay(minutes=120)
    #  aspirate liquid off of plate
    #  proceed to plate washes or pause again to flick then
    #  proceed to plate washes


def add_samples(protocol: ProtocolContext, plate: Labware,
                p300_multi: InstrumentContext, tuberack: Labware):
    """

    Args:
        protocol:
        plate:
        p300_multi:
        tuberack:

    Returns:

    """
#     max # samples = 24
#


def add_standard(protocol: ProtocolContext, plate: Labware,
                p300_multi: InstrumentContext, tuberack: Labware):
    """

    Args:
        protocol:
        plate:
        p300_multi:
        tuberack:

    Returns:

    """


