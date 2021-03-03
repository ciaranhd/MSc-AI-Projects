import numpy as np
from collections import defaultdict
import math
import copy

# =================================================================================================================#
# Import Data
training_spam = np.loadtxt(open("data/training_spam.csv"), delimiter=",").astype(np.int)
testing_spam = np.loadtxt(open("data/testing_spam.csv"), delimiter=",").astype(np.int)
# =================================================================================================================#



# =================================================================================================================#
# The Original Split of Training and Testing Data is Too Low. Risk of Underfitting. ACTION: Amend Test/Train Split
# 1) Combine Testing and Training Data.
#all_data = np.append(training_spam, testing_spam, axis=0)
#all_data = np.asarray(all_data)

# 2) Find The Row Location You Wish To Split The New NdArray From
#split_row_location =  int(0.66666666666666*len(all_data))

# 3) Split The Row Using Numpy Slicing Functions
#all_training_spam = all_data[:split_row_location,:]
#all_testing_spam = all_data[split_row_location:,:]

#print(all_training_spam.shape)
#print(all_testing_spam.shape)

#print("Shape of the spam testing data set:", testing_spam.shape)
#print("Shape of the spam training data set:", training_spam.shape)

# =================================================================================================================#




# =================================================================================================================#
# This Class Will Take Training Data And Return


# =================================================================================================================#
#               A Class To Create An Object That We Can Train Data Using A Bayesisn Model                          #
class SpamClassifier:
    def __init__(self, k):
        self.total_emails_in_training_set = k
        self.spam_dictionary = defaultdict(float)
        self.ham_dictionary = defaultdict(float)
        self.spam_probability_class_prior = None
        self.ham_probability_class_prior = None
        self.no_spam_emails = None
        self.no_ham_emails = None
        self.spam_array = None
        self.ham_array = None
        self.training_spam = None

# =================================================================================================================#
# Takes Training Data of Shape (X, 55) And Builds Two Dictionaries, Storing P(Word=w | Class =c) For Each Word     #
# For Both Spam and Ham                                                                                            #
# =================================================================================================================#
    def train(self, training_spam):
        print("Training New")
        print(f"Shape of Training Data is: {training_spam.shape}")

        # First We Need The Class Priors. P(Ham) & P(Spam) For The Training Data. 1) Retrieve Labels & Count Freq
        # of Zeros (Ham), Ones (Spam). 3) Divide By Total (training_spam.shape[0]). P(Spam) = c39% & P(Ham) = c61%
        training_labels = copy.deepcopy(training_spam[:, 0])
        no_spam_emails = np.count_nonzero(training_labels)
        no_ham_emails = training_spam.shape[0] - no_spam_emails
        self.spam_probability_class_prior = no_spam_emails / training_spam.shape[0]
        self.ham_probability_class_prior = 1 - self.spam_probability_class_prior

        # We Now Separate The Training Data Into Two Arrays, Ham and Spam
        self.spam_array = training_spam[training_spam[:, 0] == 1]
        self.ham_array = training_spam[training_spam[:, 0] == 0]

        # We need to Find P(Class = Ham | Words) & P(Class = Spam | Words) For Every Email. Action1) Remove Labels
        # There Should Be Shape (X, 54)
        spam_array_ex_label = self.spam_array[:, 1:]
        ham_array_ex_label = self.ham_array[:, 1:]


        # Find P(Word | Class = c) For Every Word. "spam_word_count" Contains The Numbers Of Messages That Given Word
        # Appears In The Set of Spam Messages

        # THIS NEEDS RENAMED. It is NOT the Number of Spam Emails, But The Sum of The Frequencies For Each Word
        # In Our Vocabulary That Appear In The Spam Class
        no_spam_emails = 0
        no_ham_emails = 0
        for i in range(spam_array_ex_label.shape[1]):
            no_spam_emails += np.count_nonzero(spam_array_ex_label[:, i])
            no_ham_emails += np.count_nonzero(ham_array_ex_label[:, i])

        alpha = 1.00
        for i in range(spam_array_ex_label.shape[1]):
            spam_word_count = np.count_nonzero(spam_array_ex_label[:, i])
            ham_word_count = np.count_nonzero(ham_array_ex_label[:, i])

            # Laplacian: Some Words May Not Appear (Word Count is Zero). This Causes OverFitting. Laplacian
            # Is Used To Adjust For Words That Do Not Appear In a Given Class.
            self.spam_dictionary[i] = (spam_word_count + alpha) / (no_spam_emails + (alpha * 2.00))
            self.ham_dictionary[i] = (ham_word_count + alpha) / (no_ham_emails + (alpha * 2.00))

# =================================================================================================================#
# Now That We Have Stored All Of The Probabilities, We Can Use Them To Find The Probability That An Email Is Spam  #
# Or Ham, Given The Words Inside It                                                                                #
# =================================================================================================================#
    def predict(self, data):
        classifier_array = np.zeros(data.shape[0])
        for i in range(data.shape[0]):
            email = data[i, :]
            probability_word_is_spam = 0.00
            probability_word_is_ham = 0.00
            for j in range(len(email)):
                if email[j] == 1:
                    probability_word_is_spam += math.log(self.spam_dictionary[j])
                    probability_word_is_ham += math.log(self.ham_dictionary[j])

            # Update With the Prior Class Probabilities
            probability_word_is_spam += math.log(self.spam_probability_class_prior)
            probability_word_is_ham += math.log(self.ham_probability_class_prior)
            # Classify
            if probability_word_is_spam > probability_word_is_ham:
                classifier_array[i] = 1
            else:
                classifier_array[i] = 0
        classifier_array = np.asarray(classifier_array)
        return classifier_array

# =================================================================================================================##
# I Split Initially Into Training (1000 Rows) and Testing (500 Rows).                                               #
# For K Fold Cross Validation I Will Further Split It New_Training (800 Rows) - Validation (200 Rows)- Testing(500 R#
# K = 5. Therefore Every Row Will Become Part Of The Validation Set At Least Once                                   #
# ==================================================================================================================#
    def k_fold_cv(self, k):
        k_fold_array_training = []
        k_fold_array_validation = []
        # Split Up Each Class Into 5 Tranches (We Are Employing A Stratified Approach So That The Final Distribution
        # Within Each Tranche Remains The Same
        ham_1, ham_2, ham_3, ham_4, ham_5 = np.array_split(copy.deepcopy(self.ham_array),k)
        ham_stratified_list = [ham_1, ham_2, ham_3, ham_4, ham_5]

        spam_1, spam_2, spam_3, spam_4, spam_5 = np.array_split(copy.deepcopy(self.spam_array), k)
        spam_stratified_list = [spam_1, spam_2, spam_3, spam_4, spam_5]

        # Merge Stratified Arrays ~ final_stratified_list Will Return 5 Arrays of Length 500, With All Having
        # A Similar Class Distribution, i.e. The Same Proportion of Ham and Spam In Each Tranche
        final_stratified_list = []
        for i in range(5):
            final_stratified_list.append(np.append(spam_stratified_list[i], ham_stratified_list[i], axis=0))
        for i in range(5):
            validation_set = final_stratified_list[i]
            training_set = None
            counter = 0
            for j in range(k):
                if j != i:
                    counter += 1
                    if counter == 1:
                        training_set = final_stratified_list[j]
                    else:
                        training_set = np.append(training_set, final_stratified_list[j], axis=0)
            if counter == 4:
                k_fold_array_training.append(training_set)
                k_fold_array_validation.append(validation_set)
        return k_fold_array_validation, k_fold_array_training



# =================================================================================================================#
#                                       CREATE OBJECT WITH TRAINING DATA

def create_classifier(training_spam):
    classifier = SpamClassifier(k=len(training_spam))
    classifier.train(training_spam)
    return classifier

# "Testing_spam" Array is Taken Directly From The I.O above. Look At Carrying out a rebalancing of testing to training
test_data = copy.deepcopy(testing_spam[:, 1:])   # add all_ if implementing more data
test_labels = copy.deepcopy(testing_spam[:, 0])   # add all_ if implementing more data
classifier = create_classifier(copy.deepcopy(training_spam))  # add all_ if implementing more data


# =================================================================================================================#
#                                            K FOLD CROSS VALIDATION                                               #
# Confirmed That All Validation and Training Arrays Are Unique
k_fold_array_validation, k_fold_array_training = classifier.k_fold_cv(5)

# THERE IS A PROBLEM WHERE WE ARE MISSING A ROW IN THE TRAINING/TESTING SPLIT

count = 0
accuracy_sum = 0
for i in range(5):
    validation_data = k_fold_array_validation[i]
    validation_features = validation_data[:, 1:]
    validation_labels = validation_data[:, 0]
    print()
    print(f"The Shape of Training Data in K Fold Iteration {i + 1} : {k_fold_array_training[i].shape}")
    kclassifier = create_classifier(k_fold_array_training[i])
    predictions = kclassifier.predict(validation_features)

    accuracy = np.count_nonzero(predictions == validation_labels) / validation_labels.shape[0]
    print(f"Accuracy of K Fold Iteration {i + 1} is {accuracy}")
    accuracy_sum += accuracy
    count += 1
print(f"Average Accuracy For Stratified Cross Validation: {accuracy_sum/count}")


# =================================================================================================================#
SKIP_TESTS = False
if not SKIP_TESTS:
    testing_spam = np.loadtxt(open("data/testing_spam.csv"), delimiter=",").astype(np.int)
    test_data = testing_spam[:, 1:]
    test_labels = testing_spam[:, 0]

    predictions = classifier.predict(test_data)
    accuracy = np.count_nonzero(predictions == test_labels)/test_labels.shape[0]
    print(f"Accuracy on test data is: {accuracy}")


