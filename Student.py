from hashlib import sha256
from random import randrange
from words import *
from datetime import datetime

class Student:
	def __init__(self, student_id="", mnemonic="", dob=None):
		if (mnemonic == "") and (student_id == ""):
			student_id = "{:05}".format(randrange(0, 10**5))  # 5-digit random identifier (string so leading 0 is preserved)
			student_id += self.generate_dob_reference(dob, student_id)
			student_id += self.generate_checksum(student_id)
		elif (mnemonic == "") or (student_id == ""):
			if mnemonic != "":
				filtered_mnemonic = "".join(letter for letter in mnemonic.lower().strip() if letter == " " or (letter.isalpha() and not letter.isnumeric()))
				words = filtered_mnemonic.split(" ")
				
				try:
					student_id = "{:03d}{:03d}{:03d}".format(adjectives.index(words[0]), adjectives.index(words[1]), nouns.index(words[2]))
					self.student_id = student_id
					self.dob = dob
				except ValueError:
					raise ValueError("One of those words is not known to this algorithm. Check your spelling and try again.")
		else:
			raise AssertionError("Cannot enter values for both student_id and mnemonic.")
		
		if self.verify_student_id(student_id, dob):
			self.student_id = student_id
			self.dob = dob
		else:
			raise ValueError("Student was created with incorrect student ID or mnemonic.")
	
	# Generators
	@staticmethod
	def generate_dob_reference(dob, salt):  # Adding salt may be unnecessary as the payload has a small number of options
		pepper = "8R6T923rC6Bx/fbv.ZWU#gTZ8[e?Bb"
		dob = "{:02d}{:02d}{:04d}{}{}".format(dob[0], dob[1], dob[2], salt, pepper)
		dob_hash = sha256(bytes(dob, encoding="utf8"))
		reference = int(dob_hash.hexdigest(), 16) % 100
		return "{:02}".format(reference)
	
	@staticmethod
	def generate_checksum(pre_checksum_id):
		total = sum(int(digit) for digit in pre_checksum_id)
		return "{:02}".format(total % 100)
	
	# Verifiers
	@staticmethod
	def verify_checksum(student_id):
		found_checksum = Student.generate_checksum(student_id[:-2])
		checksum_target = student_id[-2:]
		checksum_valid = found_checksum == checksum_target
		print("Checksum", "passed" if checksum_valid else "failed")
		return checksum_valid
	
	@staticmethod
	def verify_dob(student_id, dob):
		today = datetime.now()
		year_valid = 1 <= dob[2] <= today.year
		month_valid = 1 <= dob[1] <= 12 and not (today.year >= dob[2] and dob[1] > today.month)
		day_valid_30 = not (dob[1] in [4, 6, 9, 11]) or (1 <= dob[0] <= 30)
		day_valid_31 = not (dob[1] in [1, 3, 5, 7, 8, 10, 12]) or (1 <= dob[0] <= 31)
		day_valid_feb = not (dob[1] == 2) or (1 <= dob[0] <= 29)
		day_valid = (day_valid_30 and day_valid_31 and day_valid_feb) and not (today.year >= dob[2] and dob[1] >= today.month and dob[0] > today.day)
		dob_reference_matches = student_id[-4:-2] == Student.generate_dob_reference(dob, student_id[:-4])
		dob_valid = year_valid and month_valid and day_valid and dob_reference_matches
		print("DOB ", "correct" if dob_valid else "incorrect")
		return dob_valid
	
	@staticmethod
	def verify_student_id(student_id, dob=None):
		dob_matches = Student.verify_dob(student_id, dob) if dob is not None else True
		return student_id.isnumeric() and len(student_id) == 9 and Student.verify_checksum(student_id) and dob_matches
	
	# Getters
	def get_mnemonic(self):
		adjective_1 = adjectives[int(self.student_id[:3])]
		adjective_2 = adjectives[int(self.student_id[3:6])]
		noun = nouns[int(self.student_id[6:])]
		return adjective_1 + " " + adjective_2 + " " + noun
	
	def get_student_id(self):
		return self.student_id
	
	def get_qr_code(self):
		return "https://api.qrserver.com/v1/create-qr-code/?data=" + self.student_id
	
	# Overrides
	def __str__(self):
		return self.get_mnemonic() + " (" + self.get_student_id() + ")"
	
	def __int__(self):
		return int(self.student_id)
	
	def __lt__(self, other):
		return int(self.student_id) < int(other.student_id)
	
	def __le__(self, other):
		return int(self.student_id) <= int(other.student_id)
	
	def __eq__(self, other):
		return int(self.student_id) == int(other.student_id)
	
	def __ge__(self, other):
		return int(self.student_id) >= int(other.student_id)
	
	def __gt__(self, other):
		return int(self.student_id) > int(other.student_id)
	
	def __len__(self):
		return len(self.get_mnemonic())
