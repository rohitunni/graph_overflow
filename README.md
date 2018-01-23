# Graph Overflow

## Overview

An inordinate amount of a programmer or data scientist's time is spent searching the Internet for answers, in particular the popular website stackoverflow.com. Users submit questions and other programmers offer answers, which can be accepted by the submitter as correct.

The goal of this project is to explore how topics in SO are related in order.

## Dataset

The dataset was obtained by querying the [Stack Data Exchange](https://data.stackexchange.com/) website for all questions with an accepted answer with a 'python' or related tag. The full T-SQL query used can be found under the query.sql file in this repo.

The full dataset contained 568,697 question and answer pairs, which form the nodes of the large graph.

## Methods

The text in both question and answer body was split into "non-code" and "code" text (based on text that was placed into an html <code> tag). The non-code and code corpora were fed into gensim's multicore LDA model, with 50 topics and 2 passes each.

From the topic distributions assessed by the LDA model, each node's answer was compared by cosine similarity to every other node's question, and the 400 best neighbors for each node became an edge. The graph creation algorithm selects the questions most likely to come from the same topic distribution as answers, giving a directionality to the relations.

## Results

### Final Graph: 568,697 nodes and 227,147,087 edges

The full graph exhibits high clustering and modularity. Nodes in the graph with an 'nltk' tag, for example, have more than 10 times the number of reciprocal edges as a comparably sized random subgraph.

The graph can be mined for relations between topics.
