new_phys = []


def update_physical_addresses(phy_adds, facilities):
    for add in phy_adds.get("records"):
        print add
        for fac in facilities:
            fac_phy = fac.get("physical_addresss")
            if fac_phy:
                loc = fac_phy.pop("location_desc", None)
                if loc:
                    if add == fac_phy:
                        add["location_desc"] = loc
                        new_phys.append(add)
                        break
                    else:
                        pass

    return new_phys

# {
#                "plot_number": "6/280",
#                "town": {
#                    "name": "Rongai"
#                }
#            },

#            "physical_address": {
#            "location_desc": "Located within Olkaria 4 power
# station Kengen Naivasha",
#            "plot_number": "",
#            "town": {
#                "name": "Naivasha town"
#            }
#        },
