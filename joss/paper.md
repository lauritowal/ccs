---
title: 'CCS-Lib: A Python package to elicit latent knowledge from LLMs'
tags:
  - python
  - machine learning
  - interpretability
  - ai alignment
  - honest AI
authors: # sorted by num of commits
  - name: Walter Laurito
    corresponding: true
    affiliation: "2, 3"
    equal-contrib: true
  - name: Nora Belrose
    affiliation: 1 
    equal-contrib: true
  - name: Alex Mallen
    affiliation: "1, 7"
  - name: Kay Kozaronek
    affiliation: 2
  - name: Fabien Roger
    affiliation: 4
  - name: Christy Koh
    affiliation: 5
  - name: James Chua
    affiliation: 1
  - name: Jonathan NG
    affiliation: 2
  - name: Alexander Wan
    affiliation: 5
  - name: Reagan Lee
    affiliation: 5
  - name: Ben W.
    affiliation: 1
  - name: Kyle O'Brien
    affiliation: "1, 6"
  - name: Augustas Macijauskas
    affiliation: 8
  - name: Eric Mungai Kinuthia
    affiliation: 1
  - name: Marius PL
    affiliation: 10
  - name: Waree Sethapun
    affiliation: 9
  - name: Kaarel Hänni
    affiliation: 10

affiliations:
 - name: EleutherAI
   index: 1
 - name: FZI Research Center for Information Technology
   index: 2
 - name: Cadenza Labs
   index: 3
 - name: Redwood Research
   index: 4
 - name: UC Berkeley
   index: 5
 - name: Microsoft
   index: 6
 - name: University of Washington
   index: 7
 - name: CAML Lab, University of Cambridge
   index: 8
 - name: Princeton University
   index: 9
 - name: Independent
   index: 10
date: 11 08 2023
bibliography: paper.bib

---

# Summary

`ccs` is a library designed to elicit latent knowledge ([elk](`https://docs.google.com/document/d/1WwsnJQstPq91_Yh-Ch2XRL8H_EpsnjrC1dwZXR37PC8/`) [@christiano2021]) from language models. It includes implementations of both the original and an enhanced version of the CSS method, as well as an approach based on the Clustering—Top Principal Component (CRC-TPC) [@burns2022], called VINC. Designed for researchers, the `ccs` library offers features like multi-GPU support, integration with Huggingface and the training of supervised probes for comparisons. The Eleuther AI Discord's `elk` channel provides a platform for collaboration and discussion related to the library and associated research.

# Statement of need

The widespread adoption of language models in real-world applications presents significant challenges, particularly the potential generation of unreliable or inaccurate content [@weidinger2021ethical; @park2023ai; @evans2021truthful; @hendrycks2021unsolved]. A notable concern is that models fine-tuned on human preferences may exacerbate existing biases or lead to convincing yet misleading outputs [@perez2022].

Recent studies indicate that it's possible to extract simulated internal beliefs or 'knowledge' from language model activations [@li2022emergent; @gurnee2023language; @azaria2023internal; @bubeck2023sparks]. While supervised probing techniques can be used for this purpose [@alain2016understanding; @marks2023geometry], they rely on labels that may be compromised by human biases or limitations in human knowledge. In some cases, it's crucial to avoid human labels altogether to allow distinguishing between a model's true knowledge and its representation of human beliefs.

These considerations have led to the development of unsupervised probing methods, such as Contrast-Consistent Search (CCS) [@burns]. These techniques aim to extract knowledge embedded in language models without relying on ground truth labels [@zou2023representation; @burns2022]. Such approaches offer a promising direction for uncovering the latent knowledge within language models while mitigating the influence of human biases and limitations.

The aforementioned issues underscore the critical need for tools for researchers to easily train and investiage probes and analyze the internal representations of language models: Our `ccs` library is used to elicit latent knowledge ([elk](`https://docs.google.com/document/d/1WwsnJQstPq91_Yh-Ch2XRL8H_EpsnjrC1dwZXR37PC8/`) [@christiano2021]) from within the activations of a language model. The `ccs` library is developed to provide both the original and an enhanced version of the Contrast-Consistent Search (CCS) method described in the paper "Discovering Latent Knowledge in Language Models Without Supervision" by @burns2022.

Our enhanced version of CCS uses the LBFGS optimizer instead of Adam, which speeds up the training process. Furthermore, it uses learnable Platt scaling parameters to avoid the problem of sign ambiguity from the original implementation.

In addition, we have implemented an approach called VINC (Variance, Invariance, Negative Covariance). VINC is an enhanced method for eliciting latent knowledge from language models. It builds upon the Contrastive Representation Clustering—Top Principal Component (CRC-TPC) [@burns2022] approach and incorporates additional principles. VINC aims to find a direction in activation space that maximizes variance while encouraging negative correlation between statement pairs and paraphrase invariance. The method uses eigendecomposition to optimize a quadratic objective that balances these criteria. VINC can be seen as an alternative to CCS, which takes less time to train. Additional changes and more recent results on VINC and its successor can be found [here](https://blog.eleuther.ai/vincs/).

Finally, we provide a method to train supervised probes using logistic regression, allowing a comparison with unsupervised methods.

`ccs` serves as a tool for researchers to investigate the truthfulness of model outputs and explore the underlying beliefs embedded within the model. The library offers:

- The enhanced or original version of CCS
- Multi-GPU Support: Efficient extraction, training, and evaluation through parallel processing
- Integration with Huggingface: Easy utilization of models and datasets from a popular source
- VINC, an alternative to CCS
- Training supervised probes with logistic regression for comparisons

For collaboration, discussion, and support, the [Eleuther AI Discord's elk channel](https://discord.com/channels/729741769192767510/1070194752785489991) provides a platform for engaging with others interested in the library or related research projects.

# Acknowledgements
We would like to thank [EleutherAI](https://www.eleuther.ai/), [SERI MATS](https://www.serimats.org/) for supporting our work and [Long-Term Future Fund (LTFF)](https://funds.effectivealtruism.org/funds/far-future).