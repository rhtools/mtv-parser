HELP_TEST_ARGS = {"summary": ["summary"], "summary_with_file_env": ["summary"]}

HELP_TEST_ENVS = {"summary_with_file_env": {"mtv_file": "testfile"}}

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
        "  --file PATH  File to load  [required]\n"
        "  --help       Show this message and exit.\n"
    ),
    "summary_with_file_env": (
        " summary [OPTIONS]\n\n"
        "  Generate summary of MTV plan.\n\n"
        "Options:\n"
        "  --file PATH  File to load\n"
        "  --help       Show this message and exit.\n"
    ),
}
