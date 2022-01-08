printOutput <- function(name, output) {
  print(name)
  print('--===--===--===--===--')
  print(output$influence)
  print(output$influential_nodes)
  print('--===--===--===--===--')
}

#' @title A network of city connections
#' @name load_city_network_graph
#' @return igraph object
#' @import igraph
#' @export
load_city_network_graph <- function() {
  largest_component(graph.data.frame(read.table("dataset/city_network"), directed=FALSE))
}

graph <- load_city_network_graph()

# load_city_network_graph_nodes <- function() {
#   largest_component(read.graph("dataset/city_network_nodes", directed=FALSE))
# }
#
# graph2 <- load_city_network_graph_nodes()

generateOutput <- function(output, name, test, centrality) {
  printOutput(name, output)
  ranking <- paste0("dataset/project/", tolower(name), "-", tolower(test), "-", tolower(centrality), '-', 'ranking', ".txt")
  node_rank <- NULL
  for (node in output$influential_nodes) {
    index <- which(node == output$influential_nodes)
    node_rank[index] <- capture.output(cat(index, node))
  }

  write(node_rank, file = ranking, sep = ",",)

  budget_gaint_component <- NULL
  for (node in output$influence) {
    index <- which(node == output$influence)
    budget_gaint_component[index] <- capture.output(cat(index, node))
  }

  giant_component <- paste0("dataset/project/", tolower(name), "-", tolower(test), "-", tolower(centrality), 'giant_component', ".txt")
  write(budget_gaint_component, file = giant_component, sep = ",",)
}

budget <- 25
# budget <- 25

#DEG
# output_centrality_degree <- centrality_influential(graph, budget = budget, test_method = "RESILIENCE", centrality_method = "DEGREE")
# generateOutput(output_centrality_degree, "centrality", "RESILIENCE", "DEGREE")
#
# #DEGI
# output_adaptive_centrality_degree <- adaptive_centrality_influential(graph, budget = budget, test_method = "RESILIENCE", centrality_method = "DEGREE")
# generateOutput(output_adaptive_centrality_degree, "adaptive_centrality", "RESILIENCE", "DEGREE")
#
# #B
# output_centrality_betweenness <- centrality_influential(graph, budget = budget, test_method = "RESILIENCE", centrality_method = "BETWEENNESS")
# generateOutput(output_centrality_betweenness, "centrality", "RESILIENCE", "BETWEENNESS")
#
# #BI
# output_adaptive_centrality_betweenness <- adaptive_centrality_influential(graph, budget = budget, test_method = "RESILIENCE", centrality_method = "BETWEENNESS")
# generateOutput(output_adaptive_centrality_betweenness, "adaptive_centrality", "RESILIENCE", "BETWEENNESS")

#PageRank DEGI
output_adaptive_pagerank_degree <- adaptive_pagerank_influential(graph, budget = budget, test_method = "RESILIENCE", centrality_method = "DEGREE")
generateOutput(output_adaptive_pagerank_degree, "adaptive_pagerank", "RESILIENCE", "BETWEENNESS")

# #PageRank BI
# output_adaptive_pagerank_betweenness <- adaptive_pagerank_influential(graph, budget = budget, test_method = "RESILIENCE", centrality_method = "BETWEENNESS")
# generateOutput(output_adaptive_pagerank_betweenness, "adaptive_pagerank", "RESILIENCE", "BETWEENNESS")

#CI
# output_collective_influence <- collective_influence_influential(graph=graph, budget=budget, test_method="RESILIENCE")
# generateOutput(output_collective_influence, "collective_influence", "RESILIENCE", "")

# #CORE-HD (K-CORE + DEGI)
output_core_hd <- core_hd(graph=graph, budget = budget, test_method = "RESILIENCE")
generateOutput(output_core_hd, "corehd", "RESILIENCE", "")

#K-Core
output_coreness_influential <- coreness_influential(graph=graph, budget=budget, test_method="RESILIENCE")
generateOutput(output_coreness_influential, "coreness_influential", "RESILIENCE", "")

# #GND
output_gnd <- gnd(graph=graph, budget = budget, test_method = "RESILIENCE")
generateOutput(output_gnd, "GND", "RESILIENCE", "")

# #Local Centrality
output_local_centrality <- collective_local_centrality(graph=graph, budget=budget, neighborhood_distance=3, test_method="RESILIENCE")
generateOutput(output_local_centrality, "local_centrality", "RESILIENCE", "")
