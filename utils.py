## A collection of methods used in the master-code repository
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt


# for usage in printing output
def reverse_dict(d):
    return { v: k for (k, v) in d.iteritems() }


def dict_to_char(num_to_char_dict, list_to_find):
    return [ num_to_char_dict[x] for x in list_to_find ]


# --- TSNE: Look at tensorflow tutorial ---
# for usage in T-sne (to plot)
def plot_with_labels(low_dim_embs, labels, filename='tsne.png'):
    assert low_dim_embs.shape[0] >= len(labels), "More labels than embeddings"
    plt.figure(figsize=(18, 18)) # in inches
    for i, label in enumerate(labels):
        x, y = low_dim_embs[i, :]
        plt.scatter(x, y)
        plt.annotate(label,
            xy=(x, y),
            xytext=(5, 2),
            textcoords='offset points',
            ha='right',
            va='bottom')

    plt.savefig(filename)


# for usage in T-sne (normalized embeddings) 
def get_normalized_embeddings(model):
    try:
        import tensorflow as tf
        norm = tf.sqrt(tf.reduce_sum(tf.square(
            model.embeddings), 1, keep_dims=True))
        return model.embeddings / norm
    except ImportError:
        print("Please install tensorflow")


# T-sne
def create_tsne(model, alphadict, plot_only=100, plx=20):
    normalized_embeddings = get_normalized_embeddings(model)
    final_embeddings = normalized_embeddings.eval()
    tsne = TSNE(perplexity=plx, n_components=2, init='pca', n_iter=5000)
    low_dim_embs = tsne.fit_transform(final_embeddings[:plot_only, :])
    reverse_dictionary = alphadict#reverse_dict(alphadict)
    labels = [reverse_dictionary[i] for i in xrange(plot_only)]
    plot_with_labels(low_dim_embs, labels)
