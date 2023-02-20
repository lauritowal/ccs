"""Main entry point for `elk`."""

from .extraction import ExtractionConfig
from .list import list_runs
from .training import RunConfig
from contextlib import nullcontext, redirect_stdout
from pathlib import Path
from simple_parsing import ArgumentParser
import logging


def run():
    parser = ArgumentParser(add_help=False)
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser(
        "extract",
        help="Extract hidden states from a model.",
    ).add_arguments(ExtractionConfig, dest="extraction")

    elicit_parser = subparsers.add_parser(
        "elicit",
        help=(
            "Extract and train a set of ELK reporters "
            "on hidden states from `elk extract`. "
        ),
        conflict_handler="resolve",
    )
    elicit_parser.add_arguments(RunConfig, dest="run")
    elicit_parser.add_argument(
        "--output", "-o", type=Path, help="Path to save checkpoints to."
    )

    subparsers.add_parser(
        "eval", help="Evaluate a set of ELK reporters generated by `elk train`."
    )
    subparsers.add_parser("list", help="List all cached runs.")
    args = parser.parse_args()

    # `elk list` is a special case
    if args.command == "list":
        list_runs(args)
        return

    # Import here and not at the top to speed up `elk list`
    from .extraction.extraction_main import run as run_extraction
    from .training.train import train
    import os
    import torch.distributed as dist

    # Check if we were called with torchrun or not
    local_rank = os.environ.get("LOCAL_RANK")
    if local_rank is not None:
        dist.init_process_group("nccl")
        local_rank = int(local_rank)

    with redirect_stdout(None) if local_rank else nullcontext():
        if local_rank:
            logging.getLogger("transformers").setLevel(logging.CRITICAL)

        if args.command == "extract":
            run_extraction(args.run.data)
        elif args.command == "elicit":
            try:
                train(args.run, args.output)
            except (EOFError, FileNotFoundError):
                run_extraction(args.run.data)

                # Ensure the extraction is finished before starting training
                if dist.is_initialized():
                    dist.barrier()

                train(args.run, args.output)

        elif args.command == "eval":
            # TODO: Implement evaluation script
            raise NotImplementedError
        else:
            raise ValueError(f"Unknown command {args.command}")


if __name__ == "__main__":
    run()
