import json
import dill

# _stored_ = dill.dumps(d)
# d = dill.loads(_stored_)

def save_bougs(BougBot):
    with open('data_bougs_save.json', 'w') as fp:
        # json.dump(BougBot.dict_boug, fp)
        # dico = json.dumps(BougBot.dict_boug, indent = 4)
        # json.dump(dico, fp)
        # print(BougBot.dict_boug)
        # print('\n\n')
        # print(BougBot.dict_boug[258350641498423301])
        # print('\n\n')
        # print(BougBot.dict_boug[258350641498423301].toJson())

        tmp_dict = {}
        for key, value in BougBot.dict_boug.items():
            tmp_dict[key] = value.toJson()
        
        print(tmp_dict)
        json.dump(tmp_dict, fp)


def load_bougs(BougBot):
    with open('data_bougs_save.json', 'r') as fp:
        data = json.load(fp)
        print(data)