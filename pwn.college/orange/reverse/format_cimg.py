
with open("./output", "r") as file:
    data = file.read()
    data_str = data#decode("latin1")

    # remove prepend and append
    output = data_str.replace(r"\x1b[38;2;", "")
    output = output.replace(r"\x1b[0m", "")
    output = output.replace("m", "")
    output = output.replace(";", "")
    output = output.replace("\\\\", "\\")
    
    print(output)
    print(len(output))
    actual_output = b""

    i = 0
    while i < len(output):
        #print(actual_output)
        actual_output += int.to_bytes(int(output[i:i+3]))
        actual_output += int.to_bytes(int(output[i+3:i+6]))
        actual_output += int.to_bytes(int(output[i+6:i+9]))
        actual_output += output[i+9].encode("latin1")
        i += 10

    print(actual_output)
        

with open("./test.txt", "wb") as data:
    data.write(actual_output)

with open("./test.txt", "rb") as data:
    check = data.read()
    
    i = 3
    while i < len(check):
        print(int.to_bytes(check[i]))
        i += 4

    
    






