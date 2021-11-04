def mirbase_to_seq(mirna_list, ignore_not_found=False):
    import requests
    lookup_table = {}
    with open("../Others/mature.fa", "r") as f:
        for line in f:
            access_id = line.split(" ")[1]
            line2 = next(f)
            lookup_table[access_id] = line2.strip()
    seq = []
    for mirnas in mirna_list:
        n = None
        if type(mirnas) == str or mirnas is None:
            mirnas = [mirnas]
        for mirna in mirnas:
            if mirna in lookup_table:
                n = lookup_table[mirna]
                break
            else:
                try:
                    n = requests.get("https://www.mirbase.org/cgi-bin/get_seq.pl?acc="+mirna).text.split("\n")[2].strip()
                    break
                except:
                    pass
        if n is None and not ignore_not_found:
            raise Exception(f"No sequence found for access id: {mirna}")
        seq.append(n)
    return seq

def canonical_to_mirbase(mirna_list, ignore_not_found=False):
    lookup_table = {}
    with open("../Others/aliases.txt", "r") as f:
        for line in f:
            line = line.strip()[:-1]
            access_id, aliases = line.split("\t")
            aliases = aliases.split(";")
            for alias in aliases:
                if alias in lookup_table:
                    lookup_table[alias] += [access_id]
                else:
                    lookup_table[alias] = [access_id]
    mirbase = []
    for mirna in mirna_list:
        if mirna in lookup_table:
            mirbase.append(lookup_table[mirna])
        else:
            if ignore_not_found:
                mirbase.append(None)
            else:
                raise Exception(f"Found no access id for {mirna}")
    return mirbase

def canonical_to_seq(mirna_list, ignore_not_found=False):
    mirbase = canonical_to_mirbase(mirna_list, ignore_not_found)
    return mirbase_to_seq(mirbase, ignore_not_found)
    