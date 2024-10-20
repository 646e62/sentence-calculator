import csv

from parser import (
    check_offence_type,
    check_prelim_available,
    check_section_469_offence,
    parse_quantum,
    check_cso_availablity,
    check_inadmissibility,
    check_dna_designation,
)

# Open the CSV file
with open("data/cc-offences-2024-09-16.csv") as csvfile:
    csvreader = csv.reader(csvfile)
    data = list(csvreader)


def parse_offence(offence, mode="summary"):
    """
    Parse the offence data for a given offence.
    """

    # Remove any whitespace from the offence input and convert to lowercase
    offence = offence.strip().lower()
    parsed_offence = {}

    # Find the offence in the data
    for row in data:
        if row[0] == offence:

            # Create the offence variables
            mode = check_offence_type(row)
            prelim_available = check_prelim_available(row)
            indictable_minimum_quantum = parse_quantum(row[2])
            indictable_maximum_quantum = parse_quantum(row[3])
            summary_minimum_quantum = parse_quantum(row[4])
            summary_maximum_quantum = parse_quantum(row[5])
            section_469_offence = check_section_469_offence(row[0])

            # Offence data
            parsed_offence["section"] = row[0]
            parsed_offence["description"] = row[1]
            parsed_offence["mode"] = mode
            parsed_offence["summary_minimum"] = summary_minimum_quantum
            parsed_offence["summary_maximum"] = summary_maximum_quantum
            parsed_offence["indictable_minimum"] = indictable_minimum_quantum
            parsed_offence["indictable_maximum"] = indictable_maximum_quantum

            # Procedural rights
            parsed_offence["section_469_offence"] = section_469_offence
            parsed_offence["prelim_available"] = prelim_available

            # Sentencing options
            parsed_offence["cso_available"] = check_cso_availablity(
                row[0],
                summary_minimum_quantum,
                indictable_minimum_quantum,
                indictable_maximum_quantum,
                mode,
            )

            # Collateral consequences
            parsed_offence["dna_designation"] = check_dna_designation(
                row, mode, indictable_maximum_quantum
            )
            parsed_offence["inadmissibility"] = check_inadmissibility(
                row[0], mode, indictable_maximum_quantum["amount"]
            )

            return parsed_offence

    # Return None if the offence is not found
    return None
