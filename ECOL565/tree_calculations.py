__author__ = 'asherkhb'

from sys import argv
import dendropy

tree1_file = argv[1]
tree2_file = argv[2]

tree1 = dendropy.Tree.get_from_path(tree1_file, 'newick')
tree2 = dendropy.Tree.get_from_path(tree2_file, 'newick')

sym_diff = tree1.symmetric_difference(tree2)
#sym_diff = dendropy.treecalc.symmetric_difference(tree1, tree2)
pos_neg = tree1.false_positives_and_negatives(tree2)
#pos_neg = dendropy.treecalc.false_positives_and_negatives(tree1, tree2)
euc_dist = tree1.euclidean_distance(tree2)
#euc_dist = dendropy.treecalc.euclidean_distance(tree1, tree2)
rob_fol = tree1.robinson_foulds_distance(tree2)
#rob_fol = dendropy.treecalc.robinson_foulds_distance(tree1, tree2)

print("Tree Distances")
print("- Tree 1: %s" % tree1_file)
print("- Tree 2: %s" % tree2_file)
print('Symmetric Distance: %s' % str(sym_diff))
print('False Positives and Negatives: %s' % str(pos_neg))
print('Euclidean Distance: %s' % str(euc_dist))
print('Robinson_Foulds_Distance: %s' % str(rob_fol))