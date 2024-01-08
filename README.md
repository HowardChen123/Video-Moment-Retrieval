# Enhancing Video Moment Retrieval from Text Queries: A GPT-4 Based Approach

## Overview

This repository contains the implementation of our research paper "Enhancing Video Moment Retrieval from Text Queries: A GPT-4 Based Approach". Our method innovatively uses Multimodal Large Language Models (MLLMs), specifically GPT-4, for extracting key frames from videos and generating textual descriptions. This approach facilitates efficient and accessible methodologies for Video Moment Retrieval (VMR).

## Key Features

- **Frame Extraction**: Utilizes PySceneDetect for identifying significant scene transitions in videos.
- **Frame Description**: Employs GPT-4 Vision with a Chain-of-Thought approach for generating context-rich textual descriptions of video frames.
- **Information Retrieval**: Implements semantic search techniques for video retrieval, leveraging OpenAI’s text-embedding and FAISS for managing large-scale datasets.

## Dataset

Evaluation was conducted on the MSR-VTT dataset, a popular choice for developing and testing video retrieval algorithms based on textual queries.

## Results

Our system demonstrates potential in the field of VMR, showcasing competitive results in a zero-shot context, particularly highlighted by our Recall @ k metrics.