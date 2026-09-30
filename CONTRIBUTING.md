# Contributing

Keep contributions within the documented v0.1 scope. Bought components remain TBC.

1. Describe the concrete change and its evidence boundary.
2. Preserve unknown/blocked states; never report untested rendering, slicing, or physical behavior as validated.
3. Run `python -m unittest discover -s tests -v` from the repository root.
4. Document dependencies, supported environments, manual fallback, and actual validation results for any new integration.
5. Preserve upstream attribution. Do not submit credentials, private designs, machine-specific paths, or fabricated test evidence.

For bugs, include the script, Python/OS version, a minimal non-sensitive input, expected behavior, and actual output. A passing evidence-record check does not prove printability.
