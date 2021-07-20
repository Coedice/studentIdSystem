# studentIdSystem
A system for generating student IDs that have error detection, one-way birthday verification, and mnemonics.

Features:
1. 100,000 possible users (without possible conflicts for those with the same DOB)
2. The ability to verify a date of birth with an ID, but not to deduce the DOB with the ID alone.
3. Two digit checksum for error checking. Confirms validity with 99% probability.
4. Two adjective and one noun English mnemonic for student IDs, interoperable with numerical IDs, and intended to supplant numerical IDs at the user level.
