from rapidfuzz import fuzz, process


class FuzzySyn:
    """
    An extension on fuzzy search that supports synonyms.
    'words' should be a dictionary that is formatted as such:
    {
        'word' : [...synonyms]
    }
    """

    def __init__(self, words, cache={}) -> None:
        self.words = words
        word_list = []
        synonym_map = {}
        # adding all words in dic to word list and adding them to the hash map
        for index_word in words:
            word_list.append(index_word)
            synonym_map[index_word] = index_word
            for synonym in words[index_word]:
                word_list.append(synonym)
                if synonym not in synonym_map:
                    synonym_map[synonym] = index_word
                else:
                    print("Duplicate synonym detected")

        self.word_list = word_list
        self.synonym_map = synonym_map
        self.cache = cache

    def autocomplete(self, query, limit):
        cache_index = (query, limit)
        if cache_index not in self.cache:
            res_list = process.extract(
                query, self.word_list, scorer=fuzz.WRatio, limit=limit
            )
            return_value = [self.synonym_map[i[0]] for i in res_list]
            self.cache[cache_index] = return_value

        return self.cache[cache_index]

    # def weighted_autocomplete(self, query, limit):
    #     pass
