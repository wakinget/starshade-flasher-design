# tests/test_import.py

def test_import():
    """
    Basic smoke test to ensure the package imports successfully.
    """
    import starshade_flasher
    assert hasattr(starshade_flasher, "__version__")