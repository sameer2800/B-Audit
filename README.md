# B-Audit

**TITLE**  : INTELLIGENT BUILDING  
**TEAM**: Sri Sanketh Uppalapati and Sameer Killamsetty  

## Introduction

A self-conscious home is one which can track its own lifecycle, automate its maintenance decision makings and even improve itself. Our service runs in the background and assists in making intelligent decisions i.e a balanced decision keeping cost and comfort in mind.

## Design
![alt text](https://github.com/sameer2800/B-Audit/blob/master/static/images/b-audit.png?raw=true)

## Estimated target audience

* House owners/tenants/buyers: The maintenance costs of the house can be tracked and documented. Helps them made monetary assessments.
* Service contractors: They provide service to different building equipments. They can be a company or an individual.

## Problems that can be solved

* Reduction in maintenance costs: Implementing an auction marketplace helps reduce the repair costs as there is competitive bidding.
* Automating maintenance decisions: The building electrical equipment will be logged on purchase. Pre-determined maintenance routines will be used for automating maintenance decisions. Fault detection techniques will help detect which component of the building needs fixing/maintenance.
* Tracking building performance and lifecycle: Helps track building functionality cost and reduces hassle in transferring ownership

## Estimated MVP functionality

* Each actor has a wallet and can transfer tokens
* The owner can link as many house as possible and equipments(with relevant details like guarantee etc).
* Auction marketplace
* Automated maintenance decisions using pre determined routines
* Performance monitoring and tracking dashboard(for owner and service contractor)

## Final release functionality

Including the functionalities of a MVP, the final release will have the following additional functionalities:

* Implemented fault detection
* Multi-wallet linking
* Tipping service providers(In case the service contractor is a company)

The scope can be expanded as “Intelligent Buildings” is a vast ocean open for improvements.

## EXAMPLE

Let’s take a geyser, when geyser gets damaged , the measure of the damage is stored on the blockchain. So the geyser company can take that data and can do analysis.
1. When any household device is purchased, the purchase details will be stored on smart contract.
2. Owner of the home/contract transfers  money to the dAPP.
3. Contract daemon runs in the background, finds faults in the home and posts an auction in auction market place where contractors compete for the auction. our contract chooses the right contract based on his credibility and the amount.
4. On successful repair, money gets transferred to the contractor.

This is a simple case of 1 owner in 1 house. An owner can have multiple houses
