import sys
def evaluate_grade(score):
    if score >= 80:
        return "Excellent"
    elif 50 <= score < 80:
        return "Pass"
    elif score < 50:
        return "Fail"  
    else:
        return "F"

def main():
    if len(sys.argv) > 1:
        test_score = float(sys.argv[-1])
    else:
        test_score = float(input("Enter score: "))
    result = evaluate_grade(test_score)
    print(f"Score: {test_score} -> Grade: {result}")

if __name__ == "__main__":
    main()