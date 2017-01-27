# author: Latish Khubnani
# Date: Oct. 16th 2016

import pandas as pd
import sys


class Cluster:
    """
    This is the class to represent a single cluster with mean of that cluster and the guest points in that cluster, id is to
    identify with the cluster which is created.
    """

    def __init__(self, number):
        self.id = number
        self.mean = []
        self.guest_ids = []


"""
Using global variables to keep track of the clusters using all_clusters variable, cluster_number to keep track of number
of clusters at given point of iteration, points store the un-clustered points and there co-ordinates.
total_number_of_features stores the number of dimentions / features in a given data point.
"""
all_clusters = []
cluster_number = {}

iteration_and_smallest_cluster = {}
points = []
number_of_effective_clusters = 100
total_number_of_features = None


def distance(l1, l2):
    """
    This function calculates the eucledian distance for co-ordinates of two points supplied in form of a list.
    """
    distance_square = [(x2 - x1) ** 2 for x1, x2 in zip(l1, l2)]
    return sum(distance_square)


def get_mean(original_points):
    """
    This fucntion calculates the mean of the the points
    :param original_points: the 'ID'(s) of points in a cluster
    """

    global points
    mean_result = []

    for i in range(total_number_of_features):
        sum = 0
        for index in original_points:
            sum += points[index][i]

        mean_result.append(sum / len(original_points))
    return mean_result


def get_min_distance():
    """
    This function calculates the eucledian distance for centroid co-ordinates of two clusters and returns the cluster ids
    with smallest intercluster distance
    """
    min = sys.maxsize
    min_clusters = None
    for n in all_clusters:
        for m in all_clusters:
            if n.id != m.id:
                if n.guest_ids != m.guest_ids:
                    d = distance(n.mean, m.mean)
                    if d < min:
                        min = d
                        min_clusters = (n, m)

    return min_clusters


def merge(c1, c2):
    """
    This function merges two clusters by creating the new one and assigning the all the points from the both the clusters
    to the new one. It also calculates the new mean of the cluster before removing the clusters from the all_clusters list.
    """
    global number_of_effective_clusters, all_clusters
    number_of_effective_clusters += 1
    new_cluster = Cluster(number_of_effective_clusters)
    new_cluster.guest_ids = list(set(c1.guest_ids + c2.guest_ids))
    new_cluster.mean = get_mean(new_cluster.guest_ids)
    all_clusters.append(new_cluster)

    for i, o in enumerate(all_clusters):
        if o.id == c1.id:
            del all_clusters[i]

    for i, o in enumerate(all_clusters):
        if o.id == c2.id:
            del all_clusters[i]





def perform_clustering(no_of_clusters = 3):
    """
    Function to perform clustering. prints the clusters at     no_of_clusters but performs clustering to the finish
    """
    while len(all_clusters) != 1:
        min_clusters = get_min_distance()
        iteration_and_smallest_cluster[100 - len(all_clusters)] = min(
            [len(min_clusters[0].guest_ids), len(min_clusters[1].guest_ids)])
        merge(min_clusters[0], min_clusters[1])

        # print("merged", min_clusters[0].id, " & ", min_clusters[1].id, "number of clusters", len(all_clusters),"\n", )

        if len(all_clusters) == no_of_clusters:
            for i, c in enumerate(all_clusters):
                print("Cluster ", i+1,": ", c.guest_ids, "\n")

        global cluster_number
        cluster_number[len(all_clusters)] = all_clusters


def smallest_cluster():
    for iteration, smallest_cluster_size in iteration_and_smallest_cluster.items():
        print("iteration", iteration, " smallest cluster size", smallest_cluster_size)


def main():
    """
    main function reads the data into data frame and initializes the points dictionary with original points.
    it then creates cluster from these points and calls fucntion for performing agglomerative clustering.
    """
    df = pd.read_csv("HW_07_SHOPPING_CART_v137.csv", header=0)
    df.index = df.ID
    del df['ID']
    global points
    points = {}
    for index, row in df.iterrows():
        # if(index <):
        points[index] = row.tolist()
    global all_clusters, clusters, cluster_number, total_number_of_features

    total_number_of_features = len(points[1])
    all_clusters = []
    for index, point in points.items():
        all_clusters.append(Cluster(index))
        all_clusters[index - 1].mean = point
        all_clusters[index - 1].guest_ids.append(index)

    cluster_number[len(all_clusters)] = all_clusters
    perform_clustering()
    smallest_cluster()


if __name__ == '__main__':
    main()
