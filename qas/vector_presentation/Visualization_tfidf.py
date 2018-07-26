from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from qas.vector_presentation.transform import Transform


#stackoverflow.com/questions/27494202/how-do-i-visualize-data-points-of-tf-idf-vectors-for-kmeans-clustering
class Visualization_TfIdf():
    def __init__(self, number_cluster=5,num_seeds=10,max_interations=300,labels_color_map=None,pca_num_components=2,tsne_num_component=2):
        self.number_cluser = number_cluster
        self.num_seeds = num_seeds
        self.max_interations = max_interations
        #self.label_color = labels_color_map
        self.label_color = {0:'#20b2aa',1:"#ff7373",2:"#ffe4e1",3:"#005073",4:"#4d0404",5:"#ccc0ba",6:"#4700f9",7:"#f6f900",8:"#00f91d",9:"#da8c49",}
        self.pca_num_components= pca_num_components
        self.tsne_num_component = tsne_num_component

    def fix_transform_if_tdf_matrix(self):
        transform = Transform("../data/MAILS_MON_CONSEILLER_CONS.csv")
        return transform.sklearn_tfidfvectorizer2()

    def clustering_model_function(self):
        self.clustering_model = KMeans( n_clusters=self.number_cluser, max_iter=self.max_interations, precompute_distances="auto", n_jobs=-1)
        tf_idf_matrix = self.fix_transform_if_tdf_matrix()
        self.labels = self.clustering_model.fit_predict(tf_idf_matrix)
        self.X = tf_idf_matrix.todense()
        return self.X, self.labels,self.clustering_model

    def display_pca_plot(self):
        X, labels, clustering_model = self.clustering_model_function()
        reduce_data = PCA(n_components=self.pca_num_components).fit_transform(X)
        fig,ax = plt.subplots()
        for index, instance in enumerate(reduce_data):
            #print instance, index, labels[index]
            pca_comp_1, pca_comp_2 = reduce_data[index]
            color = self.label_color[labels[index]]
            ax.scatter(pca_comp_1,pca_comp_2,c=color)
        plt.show()

    def display_TSNE_plot(self):
        X, labels, clustering_model = self.clustering_model_function()
        embeddings = TSNE(n_components=self.tsne_num_component)
        Y = embeddings.fit_transform(X)
        plt.scatter(Y[:,0],Y[:1],cmap=plt.cm.Spectral)
        plt.show()


visualization = Visualization_TfIdf()
visualization.display_pca_plot()
visualization.display_TSNE_plot()