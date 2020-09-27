import time
CHAR_LEN = 10
_display_text_value = "Sound & vibratingggg"
current_index = 0

while True:
    if len(_display_text_value) > CHAR_LEN:
        str_end = len(_display_text_value)
        if current_index > str_end:
            current_index = -str_end
        elif current_index + CHAR_LEN < str_end and current_index >= 0:
            str_end = current_index + CHAR_LEN
        if current_index < 0:
            blanks = CHAR_LEN - (str_end + current_index)
            if blanks == 0:
                current_index = 1
            print(f"'{ blanks * ' '}{_display_text_value[0:CHAR_LEN - blanks]}'")
        else:
            text = _display_text_value[current_index:str_end]
            print(f"'{_display_text_value[current_index:str_end]}{(CHAR_LEN-len(text)) * ' '}'")
        current_index += 1
    else:
        pass

    # time.sleep(0.1)
