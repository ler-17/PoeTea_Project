import urllib.request
import urllib.parse
import urllib.error
import json
import random
import keys

def poetry_pick(word):
    results = poetry_call(word).get("result", None)

    if not results:
        return None

    if type(results) == dict:
        return results

    return results[random.randint(0, len(results)-1)]

def poetry_format(poem):
    title = poem["title"]
    poet = poem["poet"]

    return title +  " by " + poet

def tea_pick(user_keywords, caffeine_prefs=None):
    f = open("tea_query_data.json")
    tea_data_dict = json.loads(f.read())
    f.close()

    if caffeine_prefs:
        pruned_tea_dict = dict()
        for tea in tea_data_dict:
            if tea_data_dict[tea]["caffeine_content"] in caffeine_prefs:
                pruned_tea_dict[tea] = tea_data_dict[tea]
        tea_data_dict = pruned_tea_dict

    keywords = []
    for word in user_keywords:
        keywords.append(word)
        synonyms = get_synonyms(word)
        for i in range(len(synonyms)):
            keywords.append(synonyms[i]["word"])

    # making out a dictionary of all teas and their score (# of keywords in description)
    tea_rankings = {}
    best_tea_score = 0
    for tea in tea_data_dict:
        tea_score = 0
        for word in keywords:
            if word in tea_data_dict[tea]["description"]:
                tea_score += 1
                if tea_score > best_tea_score:
                    best_tea_score = tea_score
        tea_rankings[tea] = tea_score

    if best_tea_score == 0:
        return None

    # compiling a list of best ranked teas
    results = []

    while(not results):
        for tea in tea_rankings:
            if tea_rankings[tea] == best_tea_score:
                results.append(tea)

    # god we're finally done.
    return results


# makes calls to the datamuse api
def get_synonyms(word):
    base_url = "https://api.datamuse.com/words"
    args = {"rel_syn":word,
            "max":3}
    return safe_get(base_url, args)

def poetry_call(word):
    base_url = "https://www.stands4.com/services/v2/poetry.php"
    args = {"uid":keys.POETRY_UID, "tokenid": keys.POETRY_TOKENID, "term": word, "format":"json"}
    return safe_get(base_url, args)

def safe_get(base_url, args):
    url = base_url + "?" + urllib.parse.urlencode(args)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    try:
        request = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(request) as response:
            data = response.read().decode()
    except urllib.error.HTTPError as e:
        print('Error from server. Error code: ', e.code)
        return None
    except urllib.error.URLError as e:
        print('Failed to reach server. Reason: ', e.reason)
        return None
    return json.loads(data)

def format_tea_keywords(tea_keywords):
    print_keywords = '"'

    if not len(tea_keywords) == 1:
        for i in range(len(tea_keywords) - 1):
            print_keywords += tea_keywords[i] + ", "
        print_keywords += 'and ' + tea_keywords[len(tea_keywords) - 1] + '"'
    else:
        print_keywords = '"' + tea_keywords[0] + '"'

    return print_keywords


def write_tea_query_data():
    # reading in the original file that we formatted for .json readability.
    f = open("teadata.json")

    data = json.loads(f.read())
    f.close()

    # formatting the data in this dictionary
    teadict = {}

    for tea in data["query"]:

        # teas will have two data values: descriptions and caffeine content.

        name = data["query"][tea]["name"]
        description = data["query"][tea]["tasteDescription"]

        caffeine_content = data["query"][tea]["caffeineLevel"]
#        tea_key = caffeine_content + ";" + description
        teadict[name] = {"description": description, "caffeine_content": caffeine_content}
    json_string = json.dumps(teadict, indent=4)
    f = open("tea_query_data.json", "w")
    f.write(json_string)
    f.close()