import json

def save_bougs(BougBot):
    with open('data_bougs_save.json', 'w') as fp:
        tmp_dict = {}
        for boug in BougBot.dict_boug.values():
            tmp_dict[boug.get_id()] = {
                'id': boug.get_id(),
                'name': boug.get_name(),
                'money':boug.get_money(),
                'last_connected':boug.get_last_connected(),
                }
        
        # print(tmp_dict)
        json.dump(tmp_dict, fp)
        print('Data successfully saved')


def load_bougs(BougBot):
    with open('data_bougs_save.json', 'r') as fp:
        data = json.load(fp)
        # print(data)
        return data