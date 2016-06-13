def main():
    global unencrypted, encrypted
    unencrypted = int (input("Enter a 3-digit number: "))

    def isolate_digits():                 # separate the 3 digits into variables
        global units, tenths, hundreths
        units = unencrypted % 10
        tenths = (unencrypted / 10) % 10
        hundreths = (unencrypted / 100) % 10

    def replace_digits():                 # perform the encryption on each digit
        global encrypted_unit, encrypted_tenths, encrypted_hendreths
        encrypted_unit = ((units + 7) % 10)
        encrypted_tenths = ((tenths + 7) % 10)
        encrypted_hendreths = ((hundreths + 7) %10)

    def swap_digit_1_with_digit_3():
        temp = encrypted_unit
        encrypted_unit = encrypted_hundreths
        encrypted_hundreths = temp

    def recompose_encrypted_number():     # create the encrypted variable
        global encrypted
        encrypted = encrypted_unit * 1 + encrypted_tenths * 10 + encrypted_hundreths * 100

    print("Unencrypted: ", unencrypted)
    print("Encrypted:   ", encrypted)

main()
