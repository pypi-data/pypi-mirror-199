from numpy.typing import ArrayLike
from sklearn.metrics import adjusted_rand_score, silhouette_score, calinski_harabasz_score
import numpy as np

def euclidean_distance(u, v):
    """
    计算两个向量的欧氏距离
    """
    return np.linalg.norm(u - v)

def evaluate_clustering(data: np.ndarray ,gold_labels: ArrayLike, pred_labels: ArrayLike, print:bool = True):
    # 计算评估指标
    ari = adjusted_rand_score(gold_labels, pred_labels)
    silhouette = silhouette_score(data, pred_labels)
    chi = calinski_harabasz_score(data, pred_labels)

    if print:
        # 输出结果
        print(f"  Adjusted Rand Index: {ari:.3f}")
        print(f"  Silhouette Score: {silhouette:.3f}")
        print(f"  Calinski-Harabasz Index: {chi:.3f}\n")
    
    return dict(
        ARI = ari,
        SS = silhouette,
        CHI = chi
    )
    
    
