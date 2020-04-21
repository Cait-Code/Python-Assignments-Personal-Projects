class Format:
    """Formatting user inputs"""

    def __init__(self, input_message, input_keyword):
        self.input_message = input_message
        self.input_keyword = input_keyword

    def __get_message(self):
        """ Removes non-alphabetical characters from input message and returns it in UPPERCASE """
        final_message = ""  # stores reformatted message
        for i in range(len(input_message)):  # loop over each character in message
            if input_message[i].isalpha():  # only include alphabetical characters
                final_message += input_message[i]  # in the reformatted message

        return final_message.upper()  # return final message in uppercase

    def __get_key(self):
        """ Removes non-alphanetical characters from input keyword and returns it in UPPERCASE """
        encoded_key = []  # stores key in ASCII code
        final_key = []  # stores shifted key

        # encode key
        for i in range(len(input_keyword)):  # loop over each character in keyword
            if input_keyword[i].isalpha():  # only include alphabetical characters
                encoded_key.append(ord(input_keyword[i].upper()))  # convert (uppercase) letters in keyword to ASCII
                final_key.append(encoded_key[i] - 64)  # where ord('A') = 64 -> Reassign to 1.

        return final_key


class Polyalphabetic:
    """Polyalphabetic Cipher."""

    def __init__(self, message, key, shift):
        self.message = message
        self.key = key
        self.shift = shift

    def __encrypt(self):
        encrypted = ""
        i = 0
        for letter in self.message:
            if ord(letter) + self.key[i] + shift <= 90:  # where ord('Z') is 90
                encrypted += (chr(ord(letter) + self.key[i] + shift))
                i += 1
            else:
                new_key = ord(letter) + self.key[i] + shift - 90
                new_letter = chr(64 + new_key)  # chr() function gets the character encoded by an ASCII code number
                encrypted += new_letter
                i += 1
        return encrypted


def get_inputs():
    userInputs = input('Provide your inputs as follows: shift;secret word;message: \n')

    if int(userInputs.split(';')[0]) < 0:
        exit()
    else:
        input_shift, input_keyword, input_message = userInputs.split(';')

        input_message = input_message.replace(" ", "")  # Remove any spaces
        input_keyword = input_keyword.replace(" ", "")  # Remove any spaces
        # If the user doesn't enter a shift, assume they mean 0 (i.e. no shift).
        if len(input_shift) == 0:
            input_shift = '0'

        input_shift = int(input_shift)  # convert str to int

    return input_shift, input_keyword, input_message,


if __name__ == "__main__":

    while True:
        input_shift, input_keyword, input_message = get_inputs()

        final_inputs = Format(input_message, input_keyword)

        message = final_inputs._Format__get_message()

        final_key = final_inputs._Format__get_key()
        # expand key to size of message
        extend_key = final_key * (len(message) // len(input_keyword))
        for i in range(len(message) % len(input_keyword)):
            extend_key.append(ord(input_keyword[i].upper()) - 64)

        key = extend_key
        shift = input_shift
        cipher = Polyalphabetic(message, key, shift)
        encrypted = cipher._Polyalphabetic__encrypt()
        print(encrypted)