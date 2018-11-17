import pickle
import numpy as np
from sklearn.preprocessing import label_binarize, MultiLabelBinarizer
from sklearn.metrics import precision_recall_curve, recall_score, precision_score
from sklearn.metrics import average_precision_score, precision_recall_fscore_support
import matplotlib.pyplot as plt
from sklearn.externals.funcsigs import signature
from collections import Counter
from itertools import cycle

def binarize(Y, c):
	res = label_binarize(Y, classes=c)
	return res 

def plot_curve(Y, f, c):
	precision = dict()
	recall = dict()
	average_precision = dict()

	n_classes = len(c)

	for i in range(n_classes):
		precision[i], recall[i], _ = precision_recall_curve(Y[:,i], f[:,i])
		average_precision[i] = average_precision_score(Y[:,i], f[:,i])

	precision["micro"], recall["micro"], _ = precision_recall_curve(Y.ravel(),
    f.ravel())
	average_precision["micro"] = average_precision_score(Y, f,
                                                     average="micro")
	print('Average precision score, micro-averaged over all classes: {0:0.2f}'
      .format(average_precision["micro"]))

	# Plot average precision_recall_curve 
	plt.figure()
	# In matplotlib < 1.5, plt.fill_between does not have a 'step' argument
	step_kwargs = ({'step': 'post'}
               if 'step' in signature(plt.fill_between).parameters
               else {})
	plt.step(recall['micro'], precision['micro'], color='r', alpha=0.2,
         where='post')
	plt.fill_between(recall["micro"], precision["micro"], alpha=0.2, color='b',
		**step_kwargs)

	plt.xlabel('Recall')
	plt.ylabel('Precision')
	plt.ylim([0.0, 1.05])
	plt.xlim([0.0, 1.0])
	plt.title('Average precision score, micro-averaged over all Gender tags: AP={0:0.2f}'
    .format(average_precision["micro"]))
	
	# plot precision-recall curve for each class and iso-f1 curves
	# setup plot details
	colors = cycle(['navY', 'turquoise', 'darkorange', 'cornflowerblue', 'teal'])

	plt.figure(figsize=(7, 8))
	f_scores = np.linspace(0.2, 0.8, num=4)
	lines = []
	labels = []

	for f_score in f_scores:
		x = np.linspace(0.01, 1)
		y = f_score * x / (2 * x - f_score)
		l, = plt.plot(x[y >= 0], y[y >= 0], color='gray', alpha=0.2)
		plt.annotate('f1={0:0.1f}'.format(f_score), xy=(0.9, y[45] + 0.02))
	
	lines.append(l)
	labels.append('ISO-f1 curves')
	l, = plt.plot(recall["micro"], precision["micro"], color='gold', lw=2)
	lines.append(l)
	labels.append('Micro-avg: A = {0:0.2f}'
	              ''.format(average_precision["micro"]))

	for i, color in zip(range(n_classes), colors):
	    l, = plt.plot(recall[i], precision[i], color=color, lw=2)
	    lines.append(l)
	    labels.append('Class {0}: A = {1:0.2f}'
	                  ''.format(i, average_precision[i]))

	fig = plt.gca()
	# fig.subplots_adjust(bottom=0.25)
	plt.xlim([0.0, 1.0])
	plt.ylim([0.0, 1.05])
	plt.xlabel('Recall')
	plt.ylabel('Precision')
	plt.title('Extension of Precision-Recall curve to multi-class')
	plt.legend(lines, labels, bbox_to_anchor=(1.0, 1.05), bbox_transform=fig.transData)
	
	# plt.draw()
	# bb = leg.get_bbox_to_anchor().inverse_transformed(fig.transAxes)
	
	# # Change to location of the legend. 
	# xOffset = 1.5
	# bb.x0 += xOffset
	# bb.x1 += xOffset
	# leg.set_bbox_to_anchor(bb, transform = fig.transAxes)

	plt.show()

def inverseProcessLabels(original, predicted, num):
	encoder = pickle.load(open('./pickle-dumps/enc', 'rb'))[num]
	print(dict(zip(encoder.classes_, encoder.transform(encoder.classes_))))

	original = [np.where(r == 1)[0].tolist() for r in original]
	original = [i for item in original for i in item]
	predicted = np.argmax(predicted, axis=1)
	predicted = [x.tolist() for x in predicted]

	orig_features = encoder.inverse_transform(original)
	pred_features = encoder.inverse_transform(predicted)

	indexes_to_be_deleted = [i for i, (x,y) in enumerate(zip(orig_features, pred_features)) if x == 'Unk' or y == 'Unk']

	original = [[i for j, i in enumerate(original) if j not in indexes_to_be_deleted]]
	predicted = [[i for j, i in enumerate(predicted) if j not in indexes_to_be_deleted]]

	# multi = MultiLabelBinarizer()
	# o_new = multi.fit(original).transform(original)
	# p_new = multi.transform(predicted)


	print(precision_recall_fscore_support(original, predicted))

def takeCareOfUnknownClasses(original, predicted, num):

	inverseProcessLabels(original, predicted,num) # get indices of all unknown labels
	# print(len(original), len(predicted))
	# original = np.asarray([i for j, i in enumerate(original) if j not in removeIndices])
	# predicted = np.asarray([i for j, i in enumerate(predicted) if j not in removeIndices])

	# print(len(original), len(predicted))
	# return original, predicted


def plot_precision_recall(Y, f, classes):
	# check if arguments are list of lists:
	# this shall be skipped if individual features are passed as args.
	if len(Y) < 10: 
		Y1, Y2, Y3, Y4, Y5, Y7 = Y 
		f1, f2, f3, f4, f5, f7 = f 
		c1, c2, c3, c4, c5, c7 = classes[:6]
	
	# takeCareOfUnknownClasses(Y3, f3, 2)

	Y = binarize(Y1, c1)
	print(Y[:10])
	plot_curve(Y, f1, c1)
	input()

	Y = binarize(Y2, c2)
	print(Y[:10])
	plot_curve(Y, f2, c2)
	input()

	Y = binarize(Y3, c3)
	print(Y[:10])
	plot_curve(Y, f3, c3)

	input()
	Y = binarize(Y4, c4)
	print(Y[:10])
	plot_curve(Y, f4, c4)

	input()
	Y = binarize(Y5, c5)
	print(Y[:10])
	plot_curve(Y, f5, c5)

	input()
	Y = binarize(Y7, c7)
	print(Y[:10])
	plot_curve(Y, f7, c7)



# for list of lists:
Y = pickle.load(open('./pickle-dumps/originals', 'rb'))
f = pickle.load(open('./pickle-dumps/predictions_rcnn_with_attention_and_roots', 'rb'))
classes = pickle.load(open('./pickle-dumps/class_labels', 'rb'))

plot_precision_recall(Y,f,classes)
