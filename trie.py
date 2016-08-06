from rcviz import callgraph, viz
from cmd import Cmd


class Node:
	def __init__(self, name):
		self.word = None
		self.nodes = {}
		self.name = name


class Trie:
	def __init__(self):
		self.root = Node("root")

	def add_word(self, word):
		trav = self.root
		for i in range(len(word)):
			if word[i] in trav.nodes:
				trav = trav.nodes[word[i]]
			else:
				trav.nodes[word[i]] = Node(word[i])
				trav = trav.nodes[word[i]]
		trav.word = word


	def _get_suggestion(self, n, ret):
		if not n:
			return
		if n.word:
			ret.append(n.word)
		if n.nodes:
			for k in n.nodes:
				self._get_suggestion(n.nodes[k], ret)

	def get_suggestion(self, preword):
		trav = self.root
		ret = []
		for i in range(len(preword)):
			if preword[i] in trav.nodes:
				trav = trav.nodes[preword[i]]
		self._get_suggestion(trav, ret)
		return ret


	def _print_trie(self, n):
		if not n:
			return
		else:
			print(n.name)
			if n.word:
				print(n.word)
			for k in n.nodes:
				self._print_trie(n.nodes[k])

	def print_trie(self):
		self._print_trie(self.root)
		return

@viz
def visualizeTrie(root):
	if not root:
		return
	else:
		visualizeTrie.track(name=root.name)
		if root.word:
			visualizeTrie.track(word=root.word)
		child_list = []
		for k in root.nodes:
			child_list.append(root.nodes[k].name)
			visualizeTrie(root.nodes[k])
		visualizeTrie.track(children=child_list)


def add_dictionaryWords(t, dictionarypath):
	fl = open(dictionarypath)
	lines = fl.readlines()
	for l in lines:
		#print("Adding word: " + l.rstrip())
		t.add_word(l.rstrip())


class MyPrompt(Cmd):
	def do_hello(self, args):
		"""Says hello. If you provide a name, it will greet you with it."""
		if len(args) == 0:
		    name = 'stranger'
		else:
		    name = args
		print "Hello, %s" % name

	def do_quit(self, args):
		"""Quits the program."""
		print "Quitting."
		raise SystemExit

	def do_maketrie(self, args):
		"""Makes a trie with /usr/share/dict/words"""
		add_dictionaryWords(t, "/usr/share/dict/words")
		print("Done creating Trie!")

	def do_suggest(self, args):
		"""Ask the trie for suggestions by inputing some prefix"""
		if len(args) != 0:
			l = t.get_suggestion(args)
			for suggestion in l:
				print(suggestion)

	def complete_suggest(self, text, line, start_index, end_index):
		if text:
			return t.get_suggestion(text)
		else:
			return []


t = Trie()
if __name__ == '__main__':
	prompt = MyPrompt()
	prompt.prompt = '> '
	prompt.cmdloop('Starting Trie Player...')
