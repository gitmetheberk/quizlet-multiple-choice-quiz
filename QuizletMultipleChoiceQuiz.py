import numpy as np
import random
import os

ALPHABET = "abcdefghijklmnopqrstuvwxyz"
QUIZLETS_DIRECTORY = "quizlets"
termsAndDefinitions = {}


def readQuizFile(filepath):
    with open(filepath) as file:
        line = file.read()
        splitLine = line.split(";;;")

    # Randomize input
    np.random.shuffle(splitLine)

    quizItems = {}
    for l in splitLine:
        if len(l) != 0:
            termAndDef = l.split("---")
            if len(termAndDef[1]) != 0:
                quizItems[termAndDef[0]] = termAndDef[1]
    
    return quizItems


def chooseQuizFile() -> str:
    files = os.listdir(QUIZLETS_DIRECTORY)

    if len(files) == 0:
        emptySetPrint()
        return chooseQuizFile()

    print("Choose a Quizlet file")
    for i, file in enumerate(files):
        print(f"{i + 1}. {file}")

    while True:
        try:
            choice = int(input("Enter the number of the file you want to choose: "))
            if choice < 1 or choice > len(files):
                print(
                    "Invalid choice. Please enter a number between 1 and ", len(files)
                )
            else:
                return os.path.join(QUIZLETS_DIRECTORY, files[choice - 1])
        except ValueError:
            print("Invalid input. Please enter a number between 1 and ", len(files))


def printAlphabetized(listToPrint: list) -> None:
    for i in range(0, len(listToPrint)):
        print("{})\n{}\n".format(ALPHABET[i], listToPrint[i]))


def emptySetPrint() -> None:
    print(
        "There are no files in the quizlets directory or the file you've selected contains no terms\n"
        "Please check that quizlets/your_file.txt exists and is properly formatted then try again"
    )
    print("Instructions:")
    print(
        "1. Create a Quizlet\n"
        "2. Click the 3 dots\n"
        "3. Click 'export'\n"
        "4. For 'Between term and definition' click custom and enter three dashes '---'\n"
        "5. For 'Between rows' click custom and enter three semi-colons ';;;'\n"
        "6. Click copy text\n"
        "7. Create a new file in the quizlets folder\n"
        "8. Paste the text in quizlet.txt in the same folder as this program\n"
        "9. Happy studying!\n"
    )
    input("Press enter to continue")


def quiz(termsAndDefinitions: dict) -> None:

    keys = list(termsAndDefinitions.keys())

    print(
        "There are {} terms in the set, good luck!\n".format(len(termsAndDefinitions))
    )

    numAnsweredCorrectly = 0
    for i in range(0, len(termsAndDefinitions)):
        answers = [termsAndDefinitions[keys[i]]]

        alreadyUsed = [i]
        while len(answers) < 4:
            r = random.randint(0, len(termsAndDefinitions) - 1)
            if r not in alreadyUsed:
                alreadyUsed.append(r)
                answers.append(termsAndDefinitions[keys[r]])

        # Randomize
        np.random.shuffle(answers)

        # Find correct answer
        correctAnswer = ALPHABET[answers.index(termsAndDefinitions[keys[i]])]

        # Print
        print("Term: ", end="")
        print(keys[i], end="\n")
        printAlphabetized(answers)
        answerChoice = input("Enter your answer: ")

        if answerChoice == correctAnswer:
            print("\nCorrect!\n")
            numAnsweredCorrectly += 1
        else:
            print("\nThe correct answer was {}".format(correctAnswer))
            input("Review the definition and press enter to continue")

        print("\n\n\n")

    percentCorrect = (float(numAnsweredCorrectly) / len(termsAndDefinitions)) * 100
    print("Study session complete!")
    print(
        "You answered {} out of {} ({}%) correctly!".format(
            numAnsweredCorrectly, len(termsAndDefinitions), round(percentCorrect)
        )
    )

    if percentCorrect >= 90:
        print("You're going to ace it!")
    elif percentCorrect >= 80:
        print("You've got this, keep studying!")
    else:
        print("Keep studying to score even higher next time!")

    input("Press enter to exit")


def main():
    global termsAndDefinitions

    termsAndDefinitions = {}
    while len(termsAndDefinitions) == 0:
        quizFile = chooseQuizFile()
        termsAndDefinitions = readQuizFile(quizFile)

    quiz(termsAndDefinitions)


if __name__ == "__main__":
    main()
