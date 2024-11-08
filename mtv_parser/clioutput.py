import io
import sys
import weakref
from typing import Any, Self

from tabulate import tabulate

from mtv_parser.models import Plan


class Output:
    def __init__(self: Self) -> None:
        # Output buffer to store output.
        self.output = io.StringIO(initial_value="\n\n", newline="\n")

        # Finalizer for flushing buffer to stdout.
        # Will be called when self is deleted or when the interpreter exits
        self._finalize = weakref.finalize(self, self.flush_output, self.output)

        # might need to track the state of this object to ensure it's closed or not
        self._closed = False

    @staticmethod
    def flush_output(output: io.StringIO, file: io.TextIOBase | None = None) -> None:
        """Write StringIO Buffer to file (or stdout).  Closes output buffer.

        Args:
            output (io.StringIO): StringIO obj containing output buffer
            file (io.TextIOBase | None, optional): File to write butter to. Defaults to stdout.
        """
        if output.closed:
            return
        # Delay setting referece to stdout so tests can capture it
        if file is None:
            file = sys.stdout
        file.write(output.getvalue())
        output.close()

    def writeline(self: Self, line: Any = "") -> None:
        """write string to output buffer.  Adds newline if line does not end with one.

        Args:
            line (str, optional): string to write to output buffer. Defaults to "".
        """
        if self._closed:
            raise ValueError("CLIOutput is already closed")
        if not isinstance(line, str):
            line: str = str(line)
        if not line.endswith("\n"):
            line = line + "\n"
        self.write(line)

    def write(self: Self, line: Any) -> None:
        """Write string to output buffer.

        Args:
            line (str): string to write to output buffer
        """
        if self._closed:
            raise ValueError("CLIOutput is already closed")
        if not isinstance(line, str):
            line: str = str(line)
        self.output.write(line)

    def close(self: Self) -> None:
        """Calls private finalizer for output buffer.  Finalizer will be closed and cannot be called again."""
        if not self._closed:
            self._finalize()
            self._closed = True

    def migration_output(self: Self, plans: list[Plan]) -> None:
        rows = []
        number_of_migrations = len(plans)
        type_of_migration = "successful" if all(plan.succeeded for plan in plans) else "failed"
        average_time = sum(plan.duration_minutes for plan in plans) / number_of_migrations
        total_number_of_vms = sum(plan.vm_count for plan in plans)
        max_minutes = max(plan.duration_minutes for plan in plans)
        min_minutes = min(plan.duration_minutes for plan in plans)
        header = f"The number of {type_of_migration} migrations:"
        sep = "-" * len(header)
        rows.append([header, number_of_migrations])
        rows.append([sep])
        rows.append(["The number of vms:", total_number_of_vms])
        rows.append(["Longest runtime in minutes: ", f"{max_minutes:.1f}"])
        rows.append(["Shortest runtime in minutes: ", f"{min_minutes:.1f}"])
        rows.append(["Average runtime in minutes: ", f"{average_time:.1f}"])
        table = tabulate(rows, tablefmt="plain")

        self.write(table)
        self.write("\n\n")
