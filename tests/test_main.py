from src.main import main


def test_main():
    assert main() is None
    assert main.__name__ == 'main'
