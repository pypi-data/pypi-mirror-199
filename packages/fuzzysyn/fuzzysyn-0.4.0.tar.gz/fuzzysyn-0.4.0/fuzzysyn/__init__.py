from rapidfuzz import fuzz, process


class FuzzySyn:
    """
    An extension on fuzzy search that supports synonyms.
    'words' should be a dictionary that is formatted as such:
    {
        'index' : [...synonyms]
    }
    Note that the index should be included in the list of synonyms.
    """

    def __init__(self, words, cache={}) -> None:
        self.words = words
        word_list = []
        synonym_map = {}
        # adding all words in dic to word list and adding them to the hash map
        for index in words:
            for synonym in words[index]:
                word_list.append(synonym)
                if synonym not in synonym_map:
                    synonym_map[synonym] = index
                else:
                    raise Exception("Received duplicate synonym")

        self.word_list = word_list
        self.synonym_map = synonym_map
        self.cache = cache

    def autocomplete(self, query, limit=10, scorer=fuzz.WRatio):
        cache_index = (query, limit)
        if cache_index not in self.cache:
            res_list = process.extract(
                query, self.word_list, scorer=scorer, limit=limit
            )
            return_value = [self.synonym_map[i[0]] for i in res_list]
            self.cache[cache_index] = return_value

        return self.cache[cache_index]
