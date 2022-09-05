from opentrons import protocol_api
import pandas as pd
import numpy as np

#from opentrons import simulate                                                 # uncomment for simulation
#protocol = simulate.get_protocol_api('2.12')                                    # uncomment for simulation

metadata = {
    'apiLevel': '2.12',
    'protocolName': 'Larp trial with handwritten lists debug3',
    'description': 'description',
    'author': 'Shreyas'
    }

#============================================================================================================
#protocol run function
#============================================================================================================

def run(protocol: protocol_api.ProtocolContext):
    protocol.home()
#============================================================================================================
    #labware & pipette definitions
#============================================================================================================
    
    tip_300 = protocol.load_labware('opentrons_96_tiprack_300ul', 11)
    tip_1000 = protocol.load_labware('opentrons_96_tiprack_1000ul', 10)   
    reservoir = protocol.load_labware('opentrons_10_tuberack_falcon_4x50ml_6x15ml_conical', 9)
    tuberack = protocol.load_labware('opentrons_24_tuberack_eppendorf_2ml_safelock_snapcap', 4)
    
    p300 = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[tip_300])
    p1000 = protocol.load_instrument('p1000_single_gen2', 'left', tip_racks=[tip_1000])
    p300.default_speed = 100
    p1000.default_speed = 100
    
#============================================================================================================
# Reading the file
#============================================================================================================

    disp_pos = np.array([
                ['A1', 'A2', 'A3', 'A4', 'A5', 'A6'],
                ['B1', 'B2', 'B3', 'B4', 'B5', 'B6'],
                ['C1', 'C2', 'C3', 'C4', 'C5', 'C6'],
                ['D1', 'D2', 'D3', 'D4', 'D5', 'D6']])
 
    disp_vol_MaBr = np.array([
                    [20, 20, 20, 20, 20, 20],
                    [22, 22, 22, 22, 22, 22],
                    [27, 27, 27, 27, 27, 27],
                    [30, 30, 30, 30, 30, 30]])
   
    disp_vol_PbBr2 = np.array([
                      [20, 22, 24, 26, 28, 30],
                      [20, 22, 24, 26, 28, 30],
                      [20, 22, 24, 26, 28, 30],
                      [20, 22, 24, 26, 28, 30]])
    
    disp_vol_Antisol = np.array([
                        [500, 500, 500, 500, 500, 500],
                        [600, 600, 600, 600, 600, 600],
                        [700, 700, 700, 700, 700, 700],
                        [750, 750, 750, 750, 750, 750]])
    

#============================================================================================================
#Aspirating and dispensing MaBr
#============================================================================================================ 

    p300.pick_up_tip(tip_300['A1'])
    gap = 90                # distance from the top of the well, in mm, at which to aspirate antisolvent      <<< ADJUST
    
    for i in range(0,4):                                     
        print(np.sum(disp_vol_MaBr,axis=1)[i])
        p300.aspirate (np.sum(disp_vol_MaBr,axis=1)[i], reservoir['A1'].top(-gap), rate = 2.0)           #Aspirates amt required for 6 dispenses
        p300.touch_tip()
        protocol.delay(5)
        for j in range(0,6):
              p300.dispense (disp_vol_MaBr[i][j], tuberack[disp_pos[i][j]].top( 0), rate= 1)        #dispense
              p300.touch_tip(radius=0.9, speed=60)
              protocol.delay(5)    
    p300.drop_tip()
    

#============================================================================================================
#Aspirating and Dispensing PbBr2
#============================================================================================================ 
    
    p300.pick_up_tip(tip_300['A2'])
    gap = 90
    for i in range(0,4):                                     
        
        p300.aspirate (np.sum(disp_vol_PbBr2,axis=1)[i], reservoir['B1'].top(-gap), rate = 2.0)           #Aspirates amt required for 6 dispenses
        p300.touch_tip()
        protocol.delay(3)
        for j in range(0,6):
              p300.dispense (disp_vol_PbBr2[i][j], tuberack[disp_pos[i][j]].top(0), rate= 1)        #dispense
              p300.touch_tip(radius=0.9, speed=60)
              protocol.delay(5)
    p300.drop_tip()

#============================================================================================================
# Aspirating and dispensing Antisolvent
#============================================================================================================ 

    p1000.pick_up_tip(tip_1000['A1'])
    gap = 51                 # distance from the top of the well, in mm, at which to aspirate antisolvent      <<< ADJUST
    
    for i in range(0,4):                                     
        for j in range(0,6):
             p1000.aspirate (disp_vol_Antisol[i][j], reservoir['A3'].top(-gap), rate = 50.0)           #Aspirates amt required for 6 dispenses
             p1000.touch_tip()
             protocol.delay(3)
             gap += (disp_vol_Antisol[i][j])*0.0018  
             p1000.dispense (disp_vol_Antisol[i][j], tuberack[disp_pos[i][j]].top(0), rate= 50)        #dispense
             protocol.delay(1)
             p1000.blow_out()
    p1000.drop_tip()

            
    
  
    