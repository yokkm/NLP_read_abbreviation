#from profanity_check import predict, predict_prob

replacements = {'1': 'i', '2': 's', '3': 'e', '4': 'a', '5': 's','0':'o','8':'ate','@':'a','$':'s','_':"",'-':"",".":""}
# Do actual replacement of digits to string


def replace_digit_string(word):
    replace_dig_str=""
    for i in word.split():
        for k,v in replacements.items():
            i = i.replace(k,v)  
        replace_dig_str = replace_dig_str+" "+i
    return replace_dig_str

#convert_text = "4r5e @$$ a55 a_s_s ar5e azz d0uch3 douch3 masterb8 nigg3r 5h1t c-0-c-k d1ld0 wh0r3f4c3"
#replace_digit_string(convert_text)
