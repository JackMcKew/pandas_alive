from dataclasses import dataclass
import typing


@dataclass
class OutputConfig:
    output_filename: str = ""
    output_type: str = "file"

    def get_output_type_filename(self) -> typing.Tuple[str, str]:
        return self.output_type, self.output_filename

    def set_output_type_filename(self, target_type: str, target_filename: str):
        self.verify_filename(target_filename)
        self.output_filename = target_filename
        self.output_type = target_type

    def verify_filename(self, target_filename: str) -> bool:
        if len(target_filename) <= 0:
            raise ValueError("Specify filename")

        if (
            isinstance(target_filename, str)
            and "." not in target_filename
            or len(target_filename.split(".")[1]) <= 0
        ):
            raise ValueError("`filename` must be provided & have an extension")

        return True
