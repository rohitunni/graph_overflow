# Graph Overflow

## Overview

An inordinate amount of a programmer or data scientist's time is spent searching the Internet for answers, in particular the popular website stackoverflow.com. Users submit questions and other programmers offer answers, which can be accepted by the submitter as correct.

The goal of this project is to explore how topics in SO are related in order.

## Dataset

The dataset was obtained by querying the [Stack Data Exchange](https://data.stackexchange.com/) website for all questions with an accepted answer with a 'python' or related tag. The full T-SQL query used can be found under the query.sql file in this repo.

The full dataset contained 568,697 question and answer pairs, which form the nodes of the large graph.
