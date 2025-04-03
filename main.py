import csv
import re
from pprint import pprint

def main():
    with open("phonebook_default.csv", encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)

    header = contacts_list[0]
    contacts_data = contacts_list[1:]

    processed_contacts = []
    for contact in contacts_data:
        full_name = " ".join(contact[:3]).strip()
        name_parts = full_name.split()

        lastname = name_parts[0] if len(name_parts) > 0 else ""
        firstname = name_parts[1] if len(name_parts) > 1 else ""
        surname = name_parts[2] if len(name_parts) > 2 else ""

        phone = contact[5]
        phone_pattern = r"(\+7|8)?[\s-]*\(?(\d{3})\)?[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})"
        match = re.match(phone_pattern, phone)

        if match:
            groups = match.groups()
            phone = f"+7({groups[1]}){groups[2]}-{groups[3]}-{groups[4]}"

        processed_contact = [
            lastname,
            firstname,
            surname,
            contact[3],
            contact[4],
            phone,
            contact[6]
        ]
        processed_contacts.append(processed_contact)

    unique_contacts = {}
    for contact in processed_contacts:
        key = (contact[0], contact[1])
        if key not in unique_contacts:
            unique_contacts[key] = contact
        else:
            existing = unique_contacts[key]
            for i in range(len(existing)):
                if not existing[i] and contact[i]:
                    existing[i] = contact[i]

    final_contacts = [header] + list(unique_contacts.values())

    pprint(final_contacts)

    with open("phonebook_updated.csv", "w", encoding="utf-8", newline='') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(final_contacts)

if __name__ == '__main__':
    main()
