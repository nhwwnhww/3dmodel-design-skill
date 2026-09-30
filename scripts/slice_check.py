"""Validate Bambu slice evidence records only; never invokes a slicer."""
from release_check import main
if __name__ == '__main__': raise SystemExit(main(only=['slice']))
