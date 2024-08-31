## Introduction

**WIP: This codebase is under active development**

Because language models are trained to predict the next token in naturally occurring text, they often reproduce common
human errors and misconceptions, even when they "know better" in some sense. More worryingly, when models are trained to
generate text that's rated highly by humans, they may learn to output false statements that human evaluators can't
detect. We aim to circumvent this issue by directly [**eliciting latent knowledge
**](https://docs.google.com/document/d/1WwsnJQstPq91_Yh-Ch2XRL8H_EpsnjrC1dwZXR37PC8/edit) (ELK) inside the activations
of a language model.

Specifically, we're building on the **Contrastive Representation Clustering** (CRC) method described in the
paper [Discovering Latent Knowledge in Language Models Without Supervision](https://arxiv.org/abs/2212.03827) by Burns
et al. (2022). In CRC, we search for features in the hidden states of a language model which satisfy certain logical
consistency requirements. It turns out that these features are often useful for question-answering and text
classification tasks, even though the features are trained without labels.

### Quick **Start**

Our code is based on [PyTorch](http://pytorch.org)
and [Huggingface Transformers](https://huggingface.co/docs/transformers/index). We test the code on Python 3.10 and
3.11.

First, create a virtual environment by using e.g. conda:

```
conda create -n ccs python==3.10
conda activate ccs
```

Clone the repository:
```
git clone https://github.com/EleutherAI/ccs.git
```

Next, install the package with `python -m pip install -e .` in the root directory. Use `python -m pip install -e .[dev]` if you'd like to contribute to the project (see **Development** section below). This should install all the necessary dependencies.

To fit reporters for the HuggingFace model `model` and dataset `dataset`, just run:

```bash
ccs elicit microsoft/deberta-v2-xxlarge-mnli imdb
```

This will automatically download the model and dataset, run the model and extract the relevant representations if they
aren't cached on disk, fit reporters on them, and save the reporter checkpoints to the `ccs-reporters` folder in your
home directory. It will also evaluate the reporter classification performance on a held out test set and save it to a
CSV file in the same folder.

The following will generate a CCS (Contrast Consistent Search) reporter instead of the CRC-based reporter, which is the
default.

```bash
ccs elicit microsoft/deberta-v2-xxlarge-mnli imdb --net ccs
```

The following command will evaluate the probe from the run naughty-northcutt on the hidden states extracted from the
model deberta-v2-xxlarge-mnli for the imdb dataset. It will result in an `eval.csv` and `cfg.yaml` file, which are
stored under a subfolder in `ccs-reporters/naughty-northcutt/transfer_eval`.

```bash
ccs eval naughty-northcutt microsoft/deberta-v2-xxlarge-mnli imdb
```

The following runs `elicit` on the Cartesian product of the listed models and datasets, storing it in a special folder
CCS_DIR/sweeps/<memorable_name>. Moreover, `--add_pooled` adds an additional dataset that pools all of the datasets
together. You can also add a `--visualize` flag to visualize the results of the sweep.

```bash
ccs sweep --models gpt2-{medium,large,xl} --datasets imdb amazon_polarity --add_pooled
```

If you just do `ccs plot`, it will plot the results from the most recent sweep.
If you want to plot a specific sweep, you can do so with:

```bash
ccs plot {sweep_name}
```

## Caching

The hidden states resulting from `ccs elicit` are cached as a HuggingFace dataset to avoid having to recompute them
every time we want to train a probe. The cache is stored in the same place as all other HuggingFace datasets, which is
usually `~/.cache/huggingface/datasets`.

## Contribution Guidelines

If you work on a new feature / fix or some other code task, make sure to create an issue and assign it to yourself.
Maybe, even share it in the elk channel of Eleuther's Discord with a small note. In this way, others know you are
working on the issue and people won't do the same thing twice 👍 Also others can contact you easily.

### Submitting a Pull-Requests
We welcome PRs to our libraries. They're an efficient way to include your fixes or improvements in our next release. Please follow these guidelines:

- Focus on either functionality changes OR widespread style issues, not both.
- Add tests for new or modified functionality if it makes sense.
- Address a single issue or feature with minimal code changes.
- Include relevant documentation in the repo or on our docs site.

#### "fork-and-pull" Git workflow:

- Fork the repository to your Github account.
- Clone the project to your local machine.
- Create a new branch with a concise, descriptive name.
- Make and commit your changes to our neww branch.
- Follow any repo-specific formatting and testing guidelines (see next section)
- Push the changes to your fork.
- Open a PR in our repository, using the PR template for efficient review.


#### Before commiting
1. Use `python -m pip install pre-commit && pre-commit install` in the root folder before your first commit.

2. Run tests

```bash
pytest
```

3. Run type checking

We use [pyright](https://github.com/microsoft/pyright), which is built into the VSCode editor. If you'd like to run it
as a standalone tool, it requires a [nodejs installation.](https://nodejs.org/en/download/)

```bash
pyright
```

4. Run the linter

We use [ruff](https://beta.ruff.rs/docs/). It is installed as a pre-commit hook, so you don't have to run it manually.
If you want to run it manually, you can do so with:

```bash
ruff . --fix
```

### Issues

Issues serve three main purposes: reporting library problems, requesting new features, and discussing potential changes before creating a Pull Request (PR). If you encounter a problem, first check if an existing Issue addresses it. If so, add your own reproduction information to that Issue instead of creating a new one. This approach prevents duplicate reports and helps maintainers understand the problem's scope. Additionally, adding a reaction (like a thumbs-up) to an existing Issue signals to maintainers that the problem affects multiple users, which can influence prioritization.

### Discussion and Contact

If you have additional questions you ask them in the elk channel of Eleuther's Discord https://discord.gg/zBGx3azzUn 
