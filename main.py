'''read dilled file
to call the dilled funciton'''

import dill
with open('/Users/yokk/read_abbre.pkl', 'rb') as f:
    abbre_df=dill.load(f)
    abbre_dict=dill.load(f)
    read_abbre=dill.load(f)
    
 #input::  read_abbre('I wolf love to  do thi @TEOTD buy me some 2MOR 420 fuckk 182 143 1432 need')
 #output:: ' I wolf love to do thi At the end of the day buy me some Tomorrow Marijuana fuckk I hate you I love you I love you2 need'
    
