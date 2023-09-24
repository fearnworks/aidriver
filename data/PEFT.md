[[Model Training]]
## Introduction to Parameter Efficient Fine Tuning

Fine-tuning is a common practice in machine learning where a model that has been pre-trained on a large dataset is used as a starting point for training on a specific task. This is done to save resources and time as training large models from scratch can be computationally expensive and time-consuming.

However, traditional fine-tuning involves modifying all the parameters of the pre-trained model, which is memory-intensive and may not be practical for low-resource hardware. This is where methods like Low Rank Adaptation (LoRA) and Adapter Transformers come into play.

## Low Rank Adaptation (LoRA)

LoRA is a method that introduces trainable rank decomposition matrices into each layer of the transformer architecture while keeping the pre-trained model weights frozen.

This is equivalent to adding additional parameters into the model that are specific to the task at hand. These additional parameters, rather than the entire set of pre-existing model parameters, are then adjusted during training. This reduces the number of parameters that need to be updated and therefore decreases the computational burden.

## Self Attention Module Parameters

LoRA operates within the Transformer architecture, specifically on the self-attention module, which is a key component of the model. The self-attention mechanism allows the model to pay varying levels of 'attention' to different parts of the input when generating the output.

The self-attention module has several weight matrices, specifically:

Wq (Query): These weights relate to the query part of the self-attention mechanism, which represents the current word or feature.

Wk (Key): These weights are associated with the key part of the self-attention mechanism, representing all the words or features that are compared to the query.

Wv (Value): These weights relate to the value part of the self-attention mechanism, representing all the words or features that are used to compute the output.

Wo (Output): This is the output weight matrix that computes the final output of the self-attention mechanism.

### Delta Weights and Low-Rank Representation

A key part of LoRA is the introduction of delta weights, which are the differences from the original pre-trained weights. Instead of modifying the weights directly, LoRA introduces these delta weights and represents them using a low-rank matrix, reducing the number of trainable parameters.

### Single Value Decomposition

This involves using a mathematical method known as Singular Value Decomposition (SVD). SVD breaks down any matrix into three separate matrices: U, S, and V(T). This technique is used to reduce the dimensionality of the matrix and hence compress the information contained in the delta weights.

U: The left singular vectors, computed as an orthonormal set of eigenvectors of A(T)@A.

S: A diagonal matrix of singular values. These are square roots of the eigenvalues of A@A(T).

V: The right singular vectors, computed as an orthonormal set of eigenvectors of A(T)@A.

This truncates the SVD of a higher rank matrix to get a low-rank approximation. We can find a reduced rank approximation (or truncated SVD) to A by setting all - but the first k largest singular values - equal to zero and using only the first k columns of U and V. We then replace by zeros the smallest singular values on the diagonal of S. After fine tuning, the low rank matrices can be reconstructed into full-rank matrices using the same decomposition technique, and the resulting adapted LLM can be used for downstream tasks in the new domain.

Decomposing a matrix into two lower-rank matrices using SVD can be advantageous:

- 1 : Compression : If the matrix has a high rank and a large number of entries, it may be computationally expensive or memory-intensive to store and process the entire matrix. By decomposing the matrix into two lower-rank matrices, we can represent the matrix in a more compressed form, which can save memory and speed up certain operations
- 2 : Noise Reduction : If the matrix has some level of noise or measurement error, the lower rank approximation obtained by truncating the singular value decomposition can help reduce the impact of that noise. The lower-rank approximation captures the most important directions
- 3 : Data Analysis : The lower rank approximation obtained by truncating the singular value decomposition can also reveal the underlying structure of the patterns in the data. For example, in image analysis, the lower-rank approximation can c apture the most important features of the image, sucvh as edges or textures, while discarding the finer, more noise-prone details

## Adapter Transformers

The Adapter Transformers method is similar to LoRA in the sense that it adds a small number of new parameters (referred to as adapters) to a pre-existing model, and these new parameters are trained on the downstream task.

This method allows different tasks to share the same pre-trained model, where each task has its own set of adapters. The advantage is that the base model can remain fixed, which reduces the overall number of parameters that need to be trained and thus lowers the computational burden.

## Conclusion

In summary, methods like LoRA and Adapter Transformers offer a more resource-efficient way to fine-tune large pre-trained models. They achieve this by introducing additional parameters to the model that are task-specific, while the original pre-trained weights remain unchanged. This reduces the computational and memory requirements, making it practical to fine-tune large models even on low-resource hardware.

LoRA + int8 quantization:

You can combine low rank adaptation with int8quantization to further optimize memory usage and speed up inference on hardware with specialized instructions for int8 operations, such as modern CPUs & AI accelerators. By reducing the precision of the weights and activations to 8-bit integers, you can reduce the memory footprint and efficiency while maintaining high accuracy. However you are constantly at risk of reducing the precision of the weights and activations that can lead to loss of information.

Resources :

[SVD and Data Compression Using Low-rank Matrix Approximation | The Clever Machine (dustinstansbury.github.io)](https://dustinstansbury.github.io/theclevermachine/svd-data-compression)