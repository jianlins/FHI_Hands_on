import csv
import random
import os
import shutil
import re
from zipfile import ZipFile, ZIP_DEFLATED
from visual import scrollPrint

corpus_zip = '../data/FHI.zip'
# what's the percentage of training set
train_percentage = 60


def splitter(corpus_zip, train_percent):
	#   you are welcome to include all the documents, but here we are just limiting the size for the workload considerations
	size = 100
	train_percent = 0.01 * train_percent
	corpus = {'bc': {1: [], 0: []},
			  'cc': {1: [], 0: []}}
	with ZipFile(corpus_zip, 'r') as myzip:
		#  Read document level annoations, differentiate whether the document is positive or negative,
		#  because we want to randomly split within positive docs or negative docs, not in a whole (why?)
		for filename in myzip.namelist():
			prefix = filename[:2]
			if filename.endswith('.ann'):
				with myzip.open(filename) as annfile:
					doc_anno_line = annfile.readline().decode("utf-8")
					print(type(doc_anno_line))
					conclusion = 0 if doc_anno_line.split('\t')[1].startswith('NE') else 1
					corpus[prefix][conclusion].append(filename[3:-4])

		for prefix in corpus.keys():
			train_zip = ZipFile(prefix + '_train.zip', mode='w', compression=ZIP_DEFLATED)
			test_zip = ZipFile(prefix + '_test.zip', mode='w', compression=ZIP_DEFLATED)
			try:
				subcorpus = corpus[prefix]
				# if you don't want to limit the size, just use  neg_doc_names = subcorpus[0]  directly
				random.shuffle(subcorpus[1])
				random.shuffle(subcorpus[0])
				subcorpus[0] = subcorpus[0][:(size - len(subcorpus[1]))]
				# split among positive documents
				split_train_test(myzip, train_zip, test_zip, prefix, subcorpus[1], train_percent)
				# split among negative documents
				split_train_test(myzip, train_zip, test_zip, prefix, subcorpus[0], train_percent)

			finally:
				train_zip.close()
				test_zip.close()


def split_train_test(corpuszip, train_zip, test_zip, prefix, subcorpus, train_percent):
	splice = round(len(subcorpus) * train_percent)
	# add sampled training set from the documents
	add_files(corpuszip, train_zip, prefix, subcorpus[:splice])
	# add the rest of the documents into testing set
	add_files(corpuszip, test_zip, prefix, subcorpus[splice:])


def add_files(corpuszip, targetzip, prefix, filenames):
	print('write ' + str(len(filenames)) + ' into file: ' + targetzip.filename)
	for doc_name in filenames:
		annfile = doc_name + '.ann'
		txtfile = doc_name + '.txt'
		targetzip.writestr(annfile, corpuszip.open(prefix + '/' + annfile).read())
		targetzip.writestr(txtfile, corpuszip.open(prefix + '/' + txtfile).read())


splitter(corpus_zip, 60)
