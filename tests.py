import json

class Tests:
    def __init__(self) -> None:
        with open("test_cases.json", "r") as f:
            self.cases = json.load(f)

    def SelectTestCase(self):
        print("Lid-Driven Cavity - Select a Reynolds Number Preset")
        for i, case in enumerate(self.cases):
            print(f"{i}: {case['name']}")

        while True:
            print("Enter the number of the preset you want to use")
            try:
                index = int(input())
                if index < len(self.cases):
                    return self.cases[index]
                else:
                    print("Incorrect please try again...")
            except ValueError:
                print("Invalid input, please enter a number...")