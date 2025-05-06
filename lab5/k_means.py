from collections import defaultdict

import numpy as np
import random


def initialize_centroids_forgy(data, k):
    # TODO implement random initialization
    return random.choices(data, k=k)


def weighted_distance(obs1, obs2):
    return np.sqrt((0.7826 * (obs1[0] - obs2[0])) ** 2 +
                   (-0.4194 * (obs1[1] - obs2[1])) ** 2 +
                   (0.9490 * (obs1[2] - obs2[2])) ** 2 +
                   (0.9565 * (obs1[3] - obs2[3])) ** 2)


def initialize_centroids_kmeans_pp(data, k):
    # TODO implement kmeans++ initizalization
    centroids = [random.choice(data)]
    for _ in range(k - 1):
        distances = []
        for observation in data:
            distances.append(min(weighted_distance(observation, centroid) for centroid in centroids))
        centroids.append(data[distances.index(max(distances))])
    return centroids


def assign_to_cluster(data, centroids):
    # TODO find the closest cluster for each data point
    assignments = []
    for observation in data:
        distances = [weighted_distance(observation, centroid) for centroid in centroids]
        assignments.append(distances.index(min(distances)))
    return assignments


def update_centroids(data, assignments):
    # TODO find new centroids based on the assignments
    clusters = defaultdict(list)
    for obs, cluster_id in zip(data, assignments):
        clusters[cluster_id].append(obs)
    new_centroids = []
    for cluster_id in sorted(clusters.keys()):
        cluster_points = clusters[cluster_id]
        if not cluster_points:
            continue
        keys = len(cluster_points[0])
        centroid = [sum(p[key] for p in cluster_points) / len(cluster_points) for key in range(keys)]
        # for key in range(keys):
        #     centroid[key] = sum(p[key] for p in cluster_points) / len(cluster_points)
        # print(centroid)
        new_centroids.append(centroid)
    return new_centroids


def mean_intra_distance(data, assignments, centroids):
    return np.sqrt(np.sum((data - centroids[assignments, :]) ** 2))


def k_means(data, num_centroids, kmeansplusplus=False):
    # centroids initizalization
    if kmeansplusplus:
        centroids = initialize_centroids_kmeans_pp(data, num_centroids)
    else:
        centroids = initialize_centroids_forgy(data, num_centroids)

    assignments = assign_to_cluster(data, centroids)
    iterations = 0
    for i in range(100):  # max number of iteration = 100
        print(f"Intra distance after {i} iterations: {mean_intra_distance(data, assignments, np.array(centroids))}")
        centroids = update_centroids(data, assignments)
        new_assignments = assign_to_cluster(data, centroids)
        if np.all(new_assignments == assignments):  # stop if nothing changed
            iterations = i
            break
        else:
            assignments = new_assignments

    return new_assignments, centroids, mean_intra_distance(data, new_assignments, np.array(centroids)), iterations
