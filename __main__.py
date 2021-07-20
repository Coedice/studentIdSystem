from Student import Student
from time import sleep

while True:
    print("Enter one of the following numbers:")
    print("1) Generate new student")
    print("2) Verify an ID/mnemonic")
    print("3) Convert between student IDs and mnemonics")
    choice = int(input("Choice: "))

    if choice == 1:
        dob = [int(input("DOB day: ")), int(input("DOB month: ")), int(input("DOB year: "))]
        student = Student(dob=dob)
        print("The generated mnemonic is:", student.get_mnemonic())
        print("The generated ID is:", student.get_student_id())
        print("QR code: " + student.get_qr_code())
    elif choice == 2:
        include_dob = input("Include DOB? (T/F): ").upper()
        dob = [int(input("DOB day: ")), int(input("DOB month: ")), int(input("DOB year: "))] if include_dob == "T" else None
        candidate_student_input = input("ID/mnemonic: ")
        student = Student(student_id=candidate_student_input, dob=dob) if candidate_student_input.isnumeric() else Student(mnemonic=candidate_student_input, dob=dob)
        print(student)
    elif choice == 3:
        conversion_input = input("ID/mnemonic: ")

        if conversion_input.isnumeric():
            print("Mnemonic:", Student(student_id=conversion_input).get_mnemonic())
        else:
            print("ID:", Student(mnemonic=conversion_input).get_student_id())
    else:
        print("Choice \"" + str(choice) + "\" is invalid. Try again.")

    sleep(2)
    print()
