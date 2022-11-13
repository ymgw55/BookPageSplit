# BookPageSplit

This repository provides a script to determine the part of a book to be assigned in a reading circle. 

## Package
This repository use [Python Fire](https://github.com/google/python-fire). Install as follows:

```bash
python -m pip install fire
```

## Usage
[An Introduction to Conditional Random Fields](https://homepages.inf.ed.ac.uk/csutton/publications/crftut-fnt.pdf) is used as an example to illustrate the usage.

First, create a yaml config file under `configs` with information on the sections to be read and the last page number. 
 As an example, we show the file [configs/An_Introduction_to_Conditional_Random_Fields.yaml](configs/An_Introduction_to_Conditional_Random_Fields.yaml). 
```yaml
sections:
  - title: Introduction
    start: 268
    sec: 1
    sub: 0
  - title: Implementation Details
    start: 271
    sec: 1
    sub: 1
  - title: Modeling
    start: 272
    sec: 2
    sub: 0
  - title: Graphical Modeling
    start: 272
    sec: 2
    sub: 1
  - title: Generative versus Discriminative Models
    start: 278
    sec: 2
    sub: 2
  - title: Linear-chain CRFs
    start: 286
    sec: 2
    sub: 3
  - title: General CRFs
    start: 290
    sec: 2
    sub: 4
  - title: Feature Engineering
    start: 293
    sec: 2
    sub: 5
  - title: Examples
    start: 298
    sec: 2
    sub: 6
  - title: Applications of CRFs
    start: 306
    sec: 2
    sub: 7
  - title: Notes on Terminology
    start: 308
    sec: 2
    sub: 8
  - title: Overview of Algorithm
    start: 310
    sec: 3
    sub: 0
  - title: Inference
    start: 313
    sec: 4
    sub: 0
  - title: Linear-Chain CRFs
    start: 314
    sec: 4
    sub: 1
  - title: Inference in Graphical Models
    start: 318
    sec: 4
    sub: 2
  - title: Implementation Concerns
    start: 328
    sec: 4
    sub: 3
  - title: Parameter Estimation
    start: 331
    sec: 5
    sub: 0 
  - title: Maximum Likelihood
    start: 332
    sec: 5
    sub: 1
  - title: Stochastic Gradient Methods
    start: 341
    sec: 5
    sub: 2
  - title: Parallelism
    start: 343
    sec: 5
    sub: 3
  - title: Approximate Training
    start: 343
    sec: 5
    sub: 4
  - title: Implementation Concerns
    start: 350
    sec: 5
    sub: 5
  - title: Related Work and Future Directions 
    start: 352
    sec: 6
    sub: 0
  - title: Related Work
    start: 352
    sec: 6
    sub: 1
  - title: Frontier Areas
    start: 359
    sec: 6
    sub: 2
end: 362
```
Second, run the script with the config file and the number of divisions as arguments. The following is an example of 4 divisions using the above config file. 
```bash
python main.py configs/An_Introduction_to_Conditional_Random_Fields.yaml 4
```

Finally, a file is generated under `results`, whose name is a combination of the config name and the number of sections.
In the file, the results of dividing the sections as evenly as possible are displayed. 
As an example, here is the contents of the file named `results/An_Introduction_to_Conditional_Random_Fields_4splits.txt` generated in the second step. 
```
0th-split: about 25 pages
1.0 Introduction                            268
1.1 Implementation Details                  271
2.0 Modeling                                272
2.1 Graphical Modeling                      272
2.2 Generative versus Discriminative Models 278
2.3 Linear-chain CRFs                       286
2.4 General CRFs                            290
=================================================
1st-split: about 25 pages
2.5 Feature Engineering                     293
2.6 Examples                                298
2.7 Applications of CRFs                    306
2.8 Notes on Terminology                    308
3.0 Overview of Algorithm                   310
4.0 Inference                               313
4.1 Linear-Chain CRFs                       314
=================================================
2nd-split: about 23 pages
4.2 Inference in Graphical Models           318
4.3 Implementation Concerns                 328
5.0 Parameter Estimation                    331
5.1 Maximum Likelihood                      332
=================================================
3rd-split: about 21 pages
5.2 Stochastic Gradient Methods             341
5.3 Parallelism                             343
5.4 Approximate Training                    343
5.5 Implementation Concerns                 350
6.0 Related Work and Future Directions      352
6.1 Related Work                            352
6.2 Frontier Areas                          359
=================================================

```

## Contribution
Everyone is welcome to contribute. 
