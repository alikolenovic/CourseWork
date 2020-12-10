# Author: Ali Kolenovic
# Assignment 5
# Program requires a csv file as input
# Given a csv file with edges and weights with either -1 or 1, calculate all triadic closures.
# I pledge my honor that I have abided by the Stevens Honor System.

from os import path
import networkx as nx
import pandas as pd

# Function returns the type of the triadic closure by summing the weights
def typeTri(tri):
    t0 = tri[0]
    t1 = tri[1]
    t2 = tri[2]
    return G[t0][t1]["trust"] + G[t0][t2]["trust"] + G[t1][t2]["trust"]

#Keep prompting the user for the csv file
while True:
    file = input("Type in Filename: ")
    if path.exists(file):
        break
    else:
        print("Does not exist.")

# Read the csv with pandas then convert it into a networkx graph for easier calculations.
df = pd.read_csv(file, names=["reviewer", "reviewee", "trust"])
G = nx.from_pandas_edgelist(df, "reviewer", "reviewee", "trust")

#----------- Basic networkx Function from Documentation -----------#
n_edges = G.number_of_edges()
print("Edges in network: " + str(n_edges))

n_self_loops = nx.number_of_selfloops(G)
print("Self-loops: " + str(n_self_loops))

totEdges = n_edges - n_self_loops
print("Edges used - TotEdges: " + str(totEdges))
#------------------------------------------------------------------#
# Count the amount of trust edges in the csv file
n_positive = 0
for u, v, a in G.edges(data=True):
    if u != v:
        if a["trust"] > 0:
            n_positive += 1
n_negative = totEdges - n_positive
p = n_positive / totEdges

print("Trust edges: " + str(n_positive) + "         Probability p: %.2f" % p)
print("Distrust edges: " + str(n_negative) + "      Probability 1 - p: %.2f" % (1 - p))
# find the amount of triadic closures in the graph.
tri = nx.triangles(G)
total_tri = int(sum(tri.values()) / 3)
print("Triangles: %i" % total_tri)

# Creates a list of edges in a triadic closure
Triads = [edge for edge in nx.enumerate_all_cliques(G) if len(edge) == 3]

# Gets the count of each specific closure by calling the function above on edge triangle.
TTTCount = TTDCount = TDDCount = DDDCount = 0
for triangle in Triads:
    t = typeTri(triangle)
    if t == 3:
        TTTCount += 1
    elif t == 1:
        TTDCount += 1
    elif t == -1:
        TDDCount += 1
    elif t == -3:
        DDDCount += 1
    else:
        print("Error on Edge Input")

# ---- Expected Calculations ---- #
pof_trust = n_positive / totEdges
pof_distrust = n_negative / totEdges

TTTProb = pof_trust ** 3
TTDProb = pof_trust ** 2 * pof_distrust * 3
TDDProb = pof_trust * pof_distrust ** 2 * 3
DDDProb = pof_distrust ** 3
# -------------------------------- #
print("\nExpected Distribution *      Actual Distribution")
print("Type percent number          Type percent number")
print("TTT  %.1f" % (TTTProb * 100) + "  %.1f" % (TTTProb * total_tri) + "      		TTT 	%.2f" % (
            TTTCount / total_tri * 100) + "   %i" % TTTCount)
print("TTD  %.1f" % (TTDProb * 100) + "  %.1f" % (TTDProb * total_tri) + "      		TTD 	%.2f" % (
            TTDCount / total_tri * 100) + "   %i" % TTDCount)
print("TDD  %.1f" % (TDDProb * 100) + "  %.1f" % (TDDProb * total_tri) + "      		TDD 	%.2f" % (
            TDDCount / total_tri * 100) + "   %i" % TDDCount)
print("DDD  %.1f" % (DDDProb * 100) + "  %.1f" % (DDDProb * total_tri) + "          		DDD 	%.2f" % (
            DDDCount / total_tri * 100) + "    %i" % DDDCount)
print("Total: 100  %.1f" % sum([TTTProb * total_tri, TTDProb * total_tri, TDDProb * total_tri,
                                DDDProb * total_tri]) + " 		    Total:    100     %i" % total_tri)
