import numpy as np


class Markov:
    cur_index = 0
    word_to_int = {}
    int_to_word = np.empty((10000),dtype="S20")
    rando = np.random.default_rng()

    # TODO: Make this expandable
    markov_chains = np.zeros((10000,10000))

    def init(self):
        source = np.genfromtxt("source.txt", dtype="str")


        prev_word_i = -1
        # Use nd_iter?
        for x in source:
            # TODO: Why do I have to do this? Shouldn't it be a string in the first place?
            # x = np.array_str(x)

            if x not in self.word_to_int:
                self.word_to_int[x] = self.cur_index
                self.int_to_word[self.cur_index] = x
                self.cur_index += 1

            word_i = self.word_to_int[x]
            
            if prev_word_i == -1:
                prev_word_i = word_i
                continue

            self.markov_chains[prev_word_i, word_i] = self.markov_chains[prev_word_i, word_i] + 1
            
            prev_word_i = word_i

        for i in np.arange(self.markov_chains.shape[0]):
            row_sum = np.sum(self.markov_chains[i, :])
            if (row_sum > 1):
                self.markov_chains[i, :] = self.markov_chains[i, :] / row_sum

    def generate(self, starting_word, num_words):
        # cur_i = int(self.rando.uniform(0, self.cur_index, 1))
        cur_i = self.word_to_int[starting_word]
        prevWord = b""
        cur_word = b""
        out = [starting_word]
        for i in np.arange(num_words):

            # print(np.sum(self.markov_chains[cur_i, : ]))
            cur_word = self.rando.choice(self.int_to_word, p=self.markov_chains[cur_i, : ])
            # print(self.markov_chains[cur_i, self.word_to_int[cur_word.decode("utf-8")]], "with highest prob:", np.max(self.markov_chains[cur_i, :]))
            cur_i = self.word_to_int[cur_word.decode("utf-8") ]
            # cur_word = self.int_to_word[np.argmax(self.markov_chains[cur_i, :])]
            while cur_word == prevWord:
                cur_word = self.rando.choice(self.int_to_word, p=self.markov_chains[cur_i, : ])


            # print("From word", prevWord, "selected word", cur_word, "with", self.markov_chains[self.word_to_int[prevWord.decode("utf-8")], cur_i], "probability, highest prob:", np.max(self.markov_chains[self.word_to_int]))
            # print(cur_word.decode("utf-8"), end=" ")

            prevWord = cur_word
            out.append(cur_word.decode("utf-8"))
        return out