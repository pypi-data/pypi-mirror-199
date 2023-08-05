import json, brotli, random
from tqdm import trange

class ModelParams:
    # how random is the response (0.0 to 1.0)
    entropy = 0.05

    # skewing multiplier for entropy (higher than 0.0)
    skew = 0.1

    # bias in token prediction (-1.0 to 1.0)
    bias = -1.0

    # how many tokens are used as context (1 to 50)
    memory = 50

    # use tqdm to print progress bars when training
    use_tqdm = True

def BiasedChoice(arr, bias):
    if bias == 0:
        return random.choice(arr)
    weights = []
    for i in range(len(arr)):
        if bias < 0:
            weights.append(1 - ((-bias * i) / len(arr)))
        else:
            weights.append((bias * i) / len(arr))
    return random.choices(population=arr, weights=weights, k=1)[0]

# The base class for a Model
# Used for inference and training
class Model:
    caches = []
    params = ModelParams()

    def load(self, bindata):
        self.caches = json.loads(brotli.decompress(bindata).decode('utf-8'))

    def dump(self):
        return brotli.compress(json.dumps(self.caches).encode('utf-8'), mode=brotli.MODE_GENERIC, quality=6)

    def train(self, tokens):
        rfun = range
        if self.params.use_tqdm:
            rfun = trange

        while len(self.caches) < self.params.memory:
            self.caches.append({})

        for idx in rfun(len(tokens)):
            for ctx in range(self.params.memory):
                try:
                    key = tokens[idx:idx+ctx+1]
                    val = tokens[idx+ctx+1]
                    if key[-1] == val: continue
                    hashable = ' '.join([ str(x) for x in key ])
                    if hashable not in self.caches[ctx]:
                        self.caches[ctx][hashable] = []
                    self.caches[ctx][hashable].append(val)
                except IndexError:
                    continue

    def predict(self, tokens):
        chances = []
        choices = []
        ci = 0
        ch = 1.0
        for ctx in range(min(self.params.memory, len(tokens)+1), 0, -1):
            key = tokens[-ctx:]
            hashable = ' '.join([ str(x) for x in key ])
            if hashable in self.caches[ctx-1]:
                choices.append(BiasedChoice(self.caches[ctx-1][hashable], self.params.bias))
                chances.append(ch)
                ch *= self.params.skew
                ci += 1 / self.params.memory
                if ci > self.params.entropy:
                    break
        if len(choices) == 0:
            return None
        return random.choices(choices, chances)[0]
