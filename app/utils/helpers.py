import pathlib as path
import logging


def get_project_root() -> path.Path:
    return path.Path(__file__).parent.parent

root_dir = get_project_root()
log_dir = root_dir / "logs"

def setup_logging(log_path: str) -> logging.Logger:
    """Set up logging configuration."""
    log_dir.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_dir / f"{log_path}.log"),
            logging.StreamHandler(),
        ],
    )

def get_prompt(path: str) -> str:
    """Read prompt template from a file."""
    prompt_path = get_project_root() / path
    try:
        with open(prompt_path, "r") as f:
            return f.read()
    except Exception as e:
        logging.error(f"Error reading prompt template from {prompt_path}: {e}")
        return ""
