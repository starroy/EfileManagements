from copy import copy


def insert_record(data_in, db):
    adhar_exists = False
    pan_exists = False
    if len(data_in["adhaar_no"]) > 0:
        occ = list(db.userdata.find({"adhaar_no": data_in["adhaar_no"]}))
        if len(occ) > 0:
            adhar_exists = True
    elif len(data_in["pan_no"]) > 0:
        occ = list(db.userdata.find({"pan_no": data_in["pan_no"]}))
        if len(occ) > 0:
            pan_exists = True
    if not adhar_exists and not pan_exists:
        # del data_in["_id"]
        db.userdata.insert_one(data_in)
        if len(data_in["adhaar_no"]) > 0:
            out = db.userdata.find({"adhaar_no": data_in["adhaar_no"]})
        elif len(data_in["pan_no"]) > 0:
            out = db.userdata.find({"pan_no": data_in["pan_no"]})
        out[0]["_id"] = str(out[0]["_id"])
        return out[0]
    else:
        data_in["_id"] = occ[0]["_id"]
        data_change = {}
        for k, v in occ[0].items():
            if k != "_id" and len(data_in[k]) > 0 and data_in[k] != occ[0][k]:
                data_change[k] = data_in[k]
            else:
                data_change[k] = occ[0][k]
        if occ[0] != data_in:
            filter = {"_id": occ[0]["_id"]}
            ret_dict = copy(data_change)
            del data_change["_id"]
            new_values = {"$set": data_change}
            db.userdata.update_one(filter, new_values)
            ret_dict["_id"] = str(ret_dict["_id"])
            return ret_dict
        else:
            data_in["_id"] = str(data_in["_id"])
            return data_in
