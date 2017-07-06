import os, sys
import pandas as pd
from tqdm import *

if __name__ == '__main__':
    # Columns: [u'Question ID', u'Fold', u'Answer', u'Category', u'Text']
    data = pd.read_csv('./question_data/questions.csv')

    # Categories: ['History', 'Science', 'Social_Science', 'Fine_Arts', 'Literature', 'Other']
    history_data = data[data['Category'].str.startswith("History")]
    science_data = data[data['Category'].str.startswith("Science")]
    social_science_data = data[data['Category'].str.startswith("Social_Science")]
    fine_arts_data = data[data['Category'].str.startswith("Fine_Arts")]
    literature_data = data[data['Category'].str.startswith("Literature")]
    other_data = data[data['Category'].str.startswith("Other")]

    # Stats
    print("History\n=======")
    print pd.DataFrame({'Count': history_data['Fold'].value_counts(),
                        'Percentage': history_data['Fold'].value_counts() / len(history_data['Fold'])})

    print("\nScience\n=======")
    print pd.DataFrame({'Count': science_data['Fold'].value_counts(),
                        'Percentage': science_data['Fold'].value_counts() / len(science_data['Fold'])})

    print("\nSocial Science\n==============")
    print pd.DataFrame({'Count': social_science_data['Fold'].value_counts(),
                        "Percentage": social_science_data['Fold'].value_counts() / len(social_science_data['Fold'])})

    print("\nFine Arts\n=========")
    print pd.DataFrame({'Count': fine_arts_data['Fold'].value_counts(),
                        "Percentage": fine_arts_data['Fold'].value_counts() / len(fine_arts_data['Fold'])})

    print("\nLiterature\n==========")
    print pd.DataFrame({'Count': literature_data['Fold'].value_counts(),
                        "Percentage": literature_data['Fold'].value_counts() / len(literature_data['Fold'])})

    print("\nOthers\n======\n")
    print pd.DataFrame({'Count': other_data['Fold'].value_counts(),
                        "Percentage": other_data['Fold'].value_counts() / len(other_data['Fold'])})

    # Make directory for processed data
    processed_dir = "./processed/"
    if not os.path.exists(processed_dir):
        os.makedirs(processed_dir)

    # Preprocessed files
    history_qids = open(processed_dir + 'histroy_qids', 'w')
    history_questions = open(processed_dir + 'histroy_questions', 'w')
    history_answers = open(processed_dir + 'histroy_answers', 'w')
    history_folds = open(processed_dir + 'histroy_folds', 'w')

    science_qids = open(processed_dir + 'science_qids', 'w')
    science_questions = open(processed_dir + 'science_questions', 'w')
    science_answers = open(processed_dir + 'science_answers', 'w')
    science_folds = open(processed_dir + 'science_folds', 'w')

    social_science_qids = open(processed_dir + 'social_science_qids', 'w')
    social_science_questions = open(processed_dir + 'social_science_questions', 'w')
    social_science_answers = open(processed_dir + 'social_science_answers', 'w')
    social_science_folds = open(processed_dir + 'social_science_folds', 'w')

    fine_arts_qids = open(processed_dir + 'fine_arts_qids', 'w')
    fine_arts_questions = open(processed_dir + 'fine_arts_questions', 'w')
    fine_arts_answers = open(processed_dir + 'fine_arts_answers', 'w')
    fine_arts_folds = open(processed_dir + 'fine_arts_folds', 'w')

    literature_qids = open(processed_dir + 'literature_qids', 'w')
    literature_questions = open(processed_dir + 'literature_questions', 'w')
    literature_answers = open(processed_dir + 'literature_answers', 'w')
    literature_folds = open(processed_dir + 'literature_folds', 'w')

    other_qids = open(processed_dir + 'other_qids', 'w')
    other_questions = open(processed_dir + 'other_questions', 'w')
    other_answers = open(processed_dir + 'other_answers', 'w')
    other_folds = open(processed_dir + 'other_folds', 'w')

    # Write files to process with dependancy tree parasing
    for category, fold, qid, question, answer in tqdm(
            zip(data.Category, data.Fold, data['Question ID'], data.Text, data.Answer)):
        question_sentences = question.split("|||")
        for sentence in question_sentences:
            if category.startswith("History"):
                history_qids.write(str(qid) + "\n")
                history_folds.write(fold + "\n")
                history_questions.write(sentence.strip() + "\n")
                history_answers.write(answer + "\n")

            elif category.startswith("Science"):
                science_qids.write(str(qid) + "\n")
                science_folds.write(fold + "\n")
                science_questions.write(sentence.strip() + "\n")
                science_answers.write(answer + "\n")

            elif category.startswith("Social_Science"):
                social_science_qids.write(str(qid) + "\n")
                social_science_folds.write(fold + "\n")
                social_science_questions.write(sentence.strip() + "\n")
                social_science_answers.write(answer + "\n")

            elif category.startswith("Fine_Arts"):
                fine_arts_qids.write(str(qid) + "\n")
                fine_arts_folds.write(fold + "\n")
                fine_arts_questions.write(sentence.strip() + "\n")
                fine_arts_answers.write(answer + "\n")

            elif category.startswith("Literature"):
                literature_qids.write(str(qid) + "\n")
                literature_folds.write(fold + "\n")
                literature_questions.write(sentence.strip() + "\n")
                literature_answers.write(answer + "\n")

            elif category.startswith("Other"):
                other_qids.write(str(qid) + "\n")
                other_folds.write(fold + "\n")
                other_questions.write(sentence.strip() + "\n")
                other_answers.write(answer + "\n")
