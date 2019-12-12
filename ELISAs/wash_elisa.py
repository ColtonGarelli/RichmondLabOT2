from opentrons import protocol_api
from opentrons.protocol_api.contexts import Labware, InstrumentContext

metadata = {'apiLevel': '2.0'}


def setup_wash(protocol: protocol_api.ProtocolContext):
    plate = protocol.load_labware('corning_96_wellplate_360ul_flat', '11')
    tiprack300_1 = protocol.load_labware('opentrons_96_tiprack_300ul', '10')
    reservoir = [protocol.load_labware('nest_12_reservoir_15ml', '9'),
                 protocol.load_labware('nest_12_reservoir_15ml', '3')]
    p300m = protocol.load_instrument('p300_multi', 'left', tip_racks=[tiprack300_1])
    return p300m, reservoir, plate


# TODO: account for not full tip boxes
def elisa_wash(protocol: protocol_api.ProtocolContext,
               p300m: InstrumentContext,
               reservoir: [Labware],
               plate: Labware,
               num_washes: int,
               wash_volume: int):
    """
    TODO: consider splitting into a load function and a remove function? this one is large. Is that modularity useful?
    # Maybe modularity is useful for multiple plates? Rather than changing this function to accommodate multiple plates
    # TODO: modularity here is almost certainly useful. Can reuse funcs for FACs prep
    Args:
        protocol: From robot
        p300m: P300 multichannel
        reservoir: A 12 well trough containing ELISA wash buffer
        plate: The plate to be washed
        num_washes: number of plate washes to perform
        wash_volume: volume of buffer to wash each well with

    Returns:
        nothing

    """
    # dispenses per aspiration to minimize movement and counter initialization
    dispenses_per_load = int(300/wash_volume)
    # Calculate extra volume
    well_counter = 0
    vol_counter = 0
    # Pick up tips
    # TODO: adjust num presses and increment
    p300m.pick_up_tip(p300m.tip_racks[0].well('A1'), presses=2, increment=.05)
    for i1 in range(num_washes):
        # reset aspiration height
        p300m.well_bottom_clearance.aspirate = 1
        index = 0
        # TODO: add disposal volume?
        """
        ~~~~~~~~~~~~~~~~~~
        Handle adding wash to plate. Calculate max number of dispenses per source load.
        Loop and increment index appropriately. This calculation would be automatic, 
        but volume removed from source well has to be tracked manually to prevent empty.
        ~~~~~~~~~~~~~~~~~~
        """
        for i2 in range(int(12/(dispenses_per_load))):
            # Establish a source well. well_counter should increment before well runs out of liquid
            # src must be established within this loop
            src = reservoir[0].columns()[well_counter]
            wells = plate.rows()[0][index: index+dispenses_per_load]
            # TODO: figure out volume count problem...works but not soon enough. well_counter iterates after two washes
            # TODO: maybe tips don't go down to bottom of well and that's why?
            p300m.distribute(volume=wash_volume, source=src, dest=wells,
                             new_tip='never', disposal_volume=0, blow_out=True)
            # Increment index by number of dispenses per aspiration
            index += dispenses_per_load
            # Count volume consumed from current trough well
            vol_counter += (.3 * 8)
            if vol_counter >= 9.7:
                # If most of the volume from the trough is gone, move to next well and reset volume count
                well_counter += 1
                vol_counter = 0
            # Tried distribute and keep getting tip already attached or tip not attached error
        """
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        Mix and dispense most of the liquid into the trash. Manual flicking still necessary.
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        """
        # Set clearance for tip for aspiration
        p300m.well_bottom_clearance.aspirate = 0.1
        # Mix and transfer volume from plate to trash.
        p300m.transfer(volume=wash_volume, source=plate.rows()[0],
                       dest=p300m.trash_container.wells(0), disposal_volume=100,
                       new_tip='never', mix_before=(2, 80), aspirate_speed=5, dispense_speed=12,
                       )
        p300m.home()
        protocol.pause(msg="{} washes done! Resume washing by clicking the 'Resume' button!".format(i1+1))
    protocol.comment("{} washes complete! You may proceed with your protocol.".format(num_washes))
    p300m.return_tip()
    p300m.home()



def load_antibodies():
    """

    Returns:

    """

    # below is for loading block/ab after washes. change range from wash number to wash number+1
    # if i1 == 3:
    #     p300.return_tip()
    #     p300.pick_up_tip(p300.tip_racks[0].well('A2'))
    #     well = reservoir[1].columns()[0]


def run(protocol: protocol_api.ProtocolContext):

    elisa_wash(protocol, *setup_wash(protocol), num_washes=3, wash_volume=100)


