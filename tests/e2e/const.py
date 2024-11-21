HELP_TEST_ARGS = {
    "summary": ["summary"],
    "summary_with_file_env": ["summary"],
}

HELP_TEST_ENVS = {
    "summary_with_file_env": {"mtv_files": '["testfile"]'},
}

HELP_TEST_OUTPUT = {
    "root": (
        "[OPTIONS] COMMAND [ARGS]...\n\n"
        "  Generate report artifacts based on MTV data.\n\n"
        "Options:\n"
        "  --help  Show this message and exit.\n"
        "\n"
        "Commands:\n"
        "  summary  Generate summary of MTV plan.\n"
    ),
    "summary": (
        " summary [OPTIONS]\n\n"
        "  Generate summary of MTV plan.\n\n"
        "Options:\n"
        "  -f, --file PATH  File to load  [required]\n"
        "  --help           Show this message and exit.\n"
    ),
    "summary_with_file_env": (
        " summary [OPTIONS]\n\n"
        "  Generate summary of MTV plan.\n\n"
        "Options:\n"
        "  -f, --file PATH  File to load\n"
        "  --help           Show this message and exit.\n"
    ),
}

ROOT_TEST_ARGS = {"empty": [], "summary": ["summary", "--file", "examples/vm-plans.yaml"]}
ROOT_TEST_ENVS = {}
ROOT_TEST_OUTPUT = {
    "empty": HELP_TEST_OUTPUT["root"],
    "summary": (
        "The number of failed migrations:  4\n"
        "--------------------------------\n"
        "The number of vms:                4\n"
        "Longest runtime in minutes:       3.6\n"
        "Shortest runtime in minutes:      0.2\n"
        "Average runtime in minutes:       1.9\n"
        "\n"
        "The number of successful migrations:  544\n"
        "------------------------------------\n"
        "The number of vms:                    544\n"
        "Longest runtime in minutes:           543.3\n"
        "Shortest runtime in minutes:            6\n"
        "Average runtime in minutes:            49.4\n"
    ),
}
