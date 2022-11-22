from project import final_score, highest_score, total_score

def main():
    test_final_score()
    test_highest_score()
    test_total_score()

def test_final_score():
    assert final_score(500) == "Well done! Your score was 500!"

def test_highest_score():
    assert highest_score([0, 100, 500]) == "Your highest score in this session was 500!"
    assert highest_score([]) == "Your highest score in this session was 0!"

def test_total_score():
    assert total_score([0, 100, 500]) == "Your total score in this playing session was 600!"

if __name__ == "__main__":
    main()