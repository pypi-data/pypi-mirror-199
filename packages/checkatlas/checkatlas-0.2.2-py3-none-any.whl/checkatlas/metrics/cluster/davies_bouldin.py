from sklearn.metrics import davies_bouldin_score


def run(count_repr, annotations):
    """

    :param count_repr:
    :param annotations:
    :return:
    """
    return davies_bouldin_score(count_repr, annotations)
