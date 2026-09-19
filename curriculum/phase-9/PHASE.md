# Phase 9 — Deep learning

About 130 hours over about 10 weeks, 19 Topics. For a Learner who has finished the math and classical ML phases (stable softmax and cross-entropy, gradient descent, numpy). At the end the Learner has built autograd from scratch, trains nets in PyTorch with their own loop, reads a training run like a mechanic, and is ready for attention and transformers in Phase 10.

Every Topic below lists:
- **Learned when** — what the Learner must show, on top of the standard rule (Exercises pass without hints, then later Spaced Reviews).
- **Teach** — the concepts the Tutor draws out through questions. The Tutor never lectures them wholesale.
- **Probe** — misconceptions the Tutor actively tests for during lessons and Spaced Reviews.
- **Sources** — the pages the Tutor teaches against.
- **Exercises** — folder names under this directory, in order.

Exercise folder layout: `exercise.md` (problem, examples, constraints, Hint Ladder, and the questions the Breakdown answers), then `starter.py` / `test.py` / `reference.py`. Exercises are Python-only. They may use numpy and PyTorch on CPU (both installed). Nothing downloads pretrained weights or datasets: every input is tiny and synthetic with fixed seeds, and each test file runs in well under 20 seconds on a laptop CPU. Numeric results are checked with tolerances on tiny tensors. The reference is only used by `scripts/verify-exercises.mjs` to prove the tests are correct; it is shown in the Breakdown once the Learner's own solution passes.

---

## 1. The neuron, MLPs and the forward pass

**Learned when:** the Learner computes a two-layer MLP forward pass by hand for a tiny input, explains why stacked linear layers without activations collapse into one, and hand-sets weights that solve XOR.

**Teach:** neuron = weighted sum + bias + activation; a layer as a matmul plus a broadcast bias; an MLP as composed layers; counting parameters; universal approximation as intuition only; stacked linear layers collapse to one linear map; XOR is not linearly separable, so a hidden layer is required; a batch as rows of X.

**Probe:** taking biological analogies literally; believing more layers automatically mean better; treating individual hidden units as interpretable; forgetting the bias when counting parameters; thinking a single-layer net can fit XOR.

**Sources:** https://d2l.ai/ (ch 5) · https://developers.google.com/machine-learning/crash-course (Neural Networks) · https://www.3blue1brown.com/topics/neural-networks (ch 1)

**Exercises:**
- `01-01-neuron-and-params` — `neuron(x, w, b, act)` and `count_params(layer_sizes)` for an MLP with biases.
- `01-02-mlp-forward` — `mlp_forward(x, layers)` with layers as (W, b, act) triples on lists of floats, checked against hand-computed outputs.
- `01-03-xor-by-hand` — return hand-set weights for a 2-2-1 network whose forward pass gets all four XOR cases right.

## 2. Activation functions

**Learned when:** the Learner implements the common activations and their derivatives, checks them numerically, and explains saturation, vanishing gradients and dead ReLUs.

**Teach:** sigmoid, tanh, ReLU, Leaky ReLU, GELU and their derivatives; saturation gives near-zero gradients, which vanish through depth; dead ReLU (always-negative pre-activation, zero gradient forever); zero-centered outputs and why tanh trains faster than sigmoid; softmax is an output activation, not a hidden one; GELU's tanh approximation vs the exact erf form.

**Probe:** using sigmoid in hidden layers by habit; worrying that ReLU is not differentiable at 0; thinking a dead ReLU recovers on its own; applying softmax between hidden layers; confusing the activation's derivative with the loss gradient.

**Sources:** https://d2l.ai/ (ch 5) · https://karpathy.ai/zero-to-hero.html (makemore part 3)

**Exercises:**
- `02-01-activations-and-derivatives` — each activation and its derivative, tested against a central-difference numeric derivative.
- `02-02-gelu-exact-vs-approx` — `gelu_exact(x)` with `math.erf` and `gelu_tanh(x)`, agreeing within tolerance over a range of inputs.
- `02-03-fraction-dead` — given a matrix of pre-activations (rows = examples), the fraction of ReLU units that are never active.

## 3. Computational graphs and backprop by hand

**Learned when:** the Learner backprops through a small expression graph on paper node by node, including a fan-out, and gets numbers that match a numeric check.

**Teach:** the computational graph as a DAG of operations; forward values stored per node; a local gradient per op; upstream × local (the chain rule) flowing backwards; gradients accumulate (sum) where a node fans out; reverse topological order; why reverse mode is cheap when the output is a scalar loss; backprop computes gradients and the optimizer learns.

**Probe:** overwriting instead of summing gradients at a reused node; calling backprop "the learning algorithm"; processing nodes in an order where a gradient is used before it is complete; adding local derivatives along a chain instead of multiplying them.

**Sources:** https://karpathy.ai/zero-to-hero.html (micrograd lecture) · https://cs231n.stanford.edu/schedule.html (lec 4) · https://www.3blue1brown.com/topics/neural-networks (ch 3–4)

**Exercises:**
- `03-01-manual-grads` — for `L = (a*b + c) * f`, return the gradient of L with respect to each input as a dict, checked numerically.
- `03-02-topo-sort-graph` — topological order of a DAG given as an adjacency dict, raising on a cycle.
- `03-03-graph-backward` — given nodes as (op, inputs) records, run a forward pass then a backward pass in reverse topological order with gradient accumulation at fan-outs.

## 4. A scalar autograd engine (micrograd)

**Learned when:** the Learner's own `Value` class trains a tiny MLP on a handful of points, and its gradients match numeric ones, including for `a + a`.

**Teach:** `Value(data, _children, _op)` with `grad` and a per-op `_backward` closure; `backward()` = topological sort then a reverse pass; building `-`, `/` and unary `-` from existing ops; `__radd__`/`__rmul__` so `2 * v` works; `grad +=` for fan-out; zeroing grads between steps; Neuron, Layer and MLP classes on top; a full training loop with a seeded init.

**Probe:** `grad =` instead of `grad +=` breaking reused nodes; forgetting zero_grad so gradients pile up across steps; hand-deriving subtraction rather than composing `a + (-b)`; calling `backward()` without setting the output grad to 1; blaming Python for slowness when the real cost is being scalar.

**Sources:** https://karpathy.ai/zero-to-hero.html (lec 1) · https://github.com/karpathy/micrograd

**Exercises:**
- `04-01-value-add-mul-tanh` — a `Value` class with `+`, `*`, `tanh` and `backward()`, matching hand-computed gradients including the `a + a` fan-out.
- `04-02-value-full-ops` — extend `Value` with `**`, `exp`, `relu`, `/`, unary `-`, `-` and reflected ops, verified by a numeric-gradient harness.
- `04-03-micrograd-mlp` — `MLP(nin, nouts)` with `parameters()` and a seeded training loop that drives the loss on four points below a threshold.

## 5. Loss functions for nets

**Learned when:** the Learner matches task → output layer → loss, knows which PyTorch losses expect logits, and explains how reduction and class weights change the effective learning rate.

**Teach:** MSE, L1 and Huber for regression; BCE-with-logits for binary; softmax cross-entropy for multiclass, computed from logits via log-sum-exp; label smoothing as a softened target; mean vs sum reduction; class weights for imbalance; the loss is what you optimize, the metric is what you report.

**Probe:** applying softmax or sigmoid before a logits-based loss (double softmax); switching from mean to sum and not noticing the LR effectively multiplied by the batch size; using accuracy as a loss; thinking label smoothing changes the argmax target.

**Sources:** https://d2l.ai/ (ch 3–4) · https://docs.pytorch.org/tutorials/beginner/basics/intro.html

**Exercises:**
- `05-01-huber` — `huber(y, yhat, delta)` and its gradient, matching MSE inside the delta band and L1 outside.
- `05-02-label-smoothing` — `label_smoothed_targets(k, target, eps)` summing to 1 with the target still the argmax.
- `05-03-weighted-ce` — `weighted_ce(logits, target, class_weights, reduction)` from raw logits via log-sum-exp, with both mean and sum reduction.

## 6. Vectorized backprop: tensors and the backprop ninja

**Learned when:** the Learner writes the backward pass of a Linear layer plus softmax cross-entropy on matrices by hand, and it matches autograd on the same weights.

**Teach:** tensors and shapes as the primary debugging tool; batched matmul gradients `dW = Xᵀ dY`, `dX = dY Wᵀ`, `db = sum(dY, axis=0)`; the backward of broadcasting is a sum over the broadcast axes; softmax-CE backward `(p − onehot) / N`; gradient checking with finite differences; numpy now that vectorization is the point.

**Probe:** assuming shapes that line up mean the gradient is right (a square matrix hides a missing transpose); forgetting to sum over the batch for the bias gradient; dividing by N in the loss but not in the gradient; treating the un-broadcast sum as optional.

**Sources:** https://karpathy.ai/zero-to-hero.html (makemore part 4) · https://cs231n.stanford.edu/schedule.html (lec 4) · https://course.fast.ai/Lessons/part2.html (lessons 13–14)

**Exercises:**
- `06-01-linear-backward` — `linear_backward(X, W, dY)` returning (dX, dW, db) in numpy, checked against finite differences.
- `06-02-unbroadcast` — `unbroadcast(grad, shape)` summing a gradient back to the shape it was broadcast from.
- `06-03-softmax-ce-backward` — `softmax_ce_backward(logits, targets)` for a batch, matching `torch.autograd` on the same tensors.

## 7. PyTorch fundamentals: tensors, autograd, nn.Module, the training loop

**Learned when:** the Learner writes the standard training loop from memory (data → model → loss → `zero_grad/backward/step`, plus eval mode and `no_grad`), and ports the micrograd MLP to PyTorch with matching gradients.

**Teach:** `torch.tensor`, dtype, device; `requires_grad` and `.backward()` filling `.grad`; `torch.no_grad()`; `nn.Module`, `nn.Linear`, `nn.Sequential`, `parameters()`; `optim.SGD`; `Dataset`/`DataLoader`; `model.train()` vs `model.eval()`; `state_dict` save and load; the call order zero_grad → forward → loss → backward → step.

**Probe:** forgetting `optimizer.zero_grad()`; skipping `model.eval()` so dropout and BatchNorm misbehave at test time; calling `.item()` inside the hot loop; in-place ops that break autograd; poking `.data` to dodge an error.

**Sources:** https://docs.pytorch.org/tutorials/beginner/basics/intro.html · https://d2l.ai/ (ch 5–6) · https://karpathy.ai/zero-to-hero.html (makemore part 1)

**Exercises:**
- `07-01-training-loop-order` — `training_loop(step_fns, batches, epochs)` driving a fake model object, tested on the exact call order of zero_grad, forward, backward and step.
- `07-02-torch-mlp-matches-micrograd` — an `nn.Module` MLP loaded with given weights whose gradients on a tiny batch match a hand-computed reference within tolerance.
- `07-03-fit-synthetic-regression` — `fit(X, y, epochs, lr)` training a small `nn.Sequential` on a seeded synthetic dataset until the MSE falls below a threshold, with `eval()` and `no_grad` used for the final score.

## 8. Optimizers and learning-rate schedules

**Learned when:** the Learner implements SGD with momentum and Adam from their update equations, and picks a warmup-plus-cosine schedule with a stated reason.

**Teach:** plain SGD; momentum as a velocity; Nesterov as a concept; RMSProp; Adam's m and v with bias correction; AdamW's decoupled weight decay; LR warmup; step and cosine decay; the LR-finder idea; gradient clipping by global norm.

**Probe:** assuming Adam always beats SGD (CNNs can generalize worse with it); believing an L2 penalty inside Adam equals weight decay; skipping bias correction and wondering why the first steps are huge; clipping each gradient element instead of the global norm.

**Sources:** https://d2l.ai/ (ch 12) · https://cs231n.stanford.edu/schedule.html (lec 3) · https://course.fast.ai/Lessons/part2.html (lesson 18)

**Exercises:**
- `08-01-sgd-momentum-step` — `sgd_momentum_step(params, grads, state, lr, beta)` updating lists in place and returning the new velocities.
- `08-02-adam-step` — `adam_step(params, grads, state, lr, b1, b2, eps, t)` with bias correction, matching a reference sequence of values.
- `08-03-cosine-warmup-and-clip` — `cosine_lr(step, total, base, warmup)` and `clip_grad_norm(grads, max_norm)` returning the pre-clip norm.

## 9. Initialization and activation/gradient statistics

**Learned when:** the Learner explains why a naive init makes the initial loss too high or saturates tanh, and fixes it with Xavier or Kaiming.

**Teach:** expected initial loss `−log(1/C)` as the first sanity check; variance propagation through a layer (fan-in); Xavier/Glorot for tanh, Kaiming/He for ReLU; the gain; symmetry breaking; vanishing and exploding activations with depth; watching activation histograms and the update-to-data ratio (about 1e-3).

**Probe:** initializing everything to zero; believing "small random" is enough for deep nets; confusing fan-in with fan-out; thinking a high initial loss is fine because it will come down.

**Sources:** https://karpathy.ai/zero-to-hero.html (makemore part 3) · https://course.fast.ai/Lessons/part2.html (lesson 17) · https://d2l.ai/ (ch 5–6)

**Exercises:**
- `09-01-expected-initial-loss` — `expected_initial_ce(num_classes)` and `too_confident_at_init(logits, tol)` flagging a logits batch whose loss is far above it.
- `09-02-kaiming-xavier` — `kaiming_std(fan_in, gain)` and `xavier_bound(fan_in, fan_out)`.
- `09-03-simulate-depth-std` — `simulate_depth_std(depth, width, init_std, act, seed)` in numpy returning the per-layer activation std, showing collapse or explosion.

## 10. Normalization: BatchNorm and LayerNorm

**Learned when:** the Learner implements BatchNorm and LayerNorm forward passes, and explains why BatchNorm behaves differently in train and eval mode while LayerNorm does not.

**Teach:** normalize → scale by γ → shift by β; BatchNorm over the batch axis with running mean/var updated by momentum; eval mode uses the running statistics; LayerNorm over the feature axis per example (the transformer's choice); eps for stability; BatchNorm's batch-coupling noise as a regularizer; the linear bias before BatchNorm is redundant.

**Probe:** BatchNorm at batch size 1; forgetting `eval()` so inference depends on the batch an example arrives with; thinking LayerNorm normalizes over the batch; treating γ and β as fixed rather than learned.

**Sources:** https://karpathy.ai/zero-to-hero.html (makemore part 3) · https://d2l.ai/ (ch 8 batch normalization) · https://course.fast.ai/Lessons/part2.html (lesson 17)

**Exercises:**
- `10-01-layernorm` — `layernorm(x, gamma, beta, eps)` per row, with mean ≈ 0 and var ≈ 1 before scale and shift.
- `10-02-batchnorm-forward` — `batchnorm_forward(batch, gamma, beta, running, momentum, training)` updating running stats only in training mode.
- `10-03-batchnorm-eval-invariance` — a `BatchNorm1d` class whose eval output for one example is identical whatever batch it is placed in.

## 11. Regularization in deep nets

**Learned when:** the Learner reads a train/val curve from a deep-net run, names the lever to pull, and implements inverted dropout that is off at eval.

**Teach:** inverted dropout scaling by 1/(1−p) at train time and identity at eval; weight decay; data augmentation (flips, crops) as free data; early stopping on validation loss; "overfit one batch first" as the sanity check before regularizing; more regularization when underfitting only hurts.

**Probe:** applying dropout at inference; thinking dropout changes the expected activation; augmenting the validation set; adding regularization to a model that has not fit the training set yet.

**Sources:** https://d2l.ai/ (ch 5 dropout) · https://course.fast.ai/Lessons/part2.html (lesson 19) · https://cs231n.stanford.edu/schedule.html (lec 3)

**Exercises:**
- `11-01-inverted-dropout` — `dropout(x, p, rng, training)` whose mean output over many seeds matches the input.
- `11-02-augment-flip-crop` — `augment_flip_crop(img, rng, crop)` on a list-of-lists image, with shape and pixel-set checks.
- `11-03-early-stopping` — `early_stopping_epoch(val_losses, patience)` returning the epoch to restore, or `None` if training never stalled.

## 12. Hyperparameter tuning methodology and experiment tracking

**Learned when:** the Learner runs a tuning study the Tuning Playbook way (fix nuisance parameters, sweep one scientific parameter, compare against a baseline) and logs every run so a result can be reproduced.

**Teach:** the Tuning Playbook loop: pick a baseline, sort hyperparameters into scientific, nuisance and fixed, run a study, decide; random search over a log-uniform range beats grid for the LR; batch size mostly trades throughput for LR, it is not a quality knob on its own; look at training curves, not only final numbers; an experiment record = config + seed + code version + metrics per step; naming runs; comparing runs on the same validation split; tracking tools (MLflow, W&B) are a table of these records.

**Probe:** sweeping several hyperparameters at once and crediting the wrong one; sampling the LR uniformly instead of log-uniformly; tuning on the test set; changing code between runs without recording it; trusting a single seed.

**Sources:** https://developers.google.com/machine-learning/guides (Deep Learning Tuning Playbook) · https://madewithml.com/ (tuning, experiment-tracking) · https://www.deeplearning.ai/courses/deep-learning-specialization/ (course 2)

**Exercises:**
- `12-01-log-uniform-search` — `sample_configs(space, n, rng)` where log-scaled ranges are sampled log-uniformly, checked by the spread of the samples.
- `12-02-run-log` — a `RunLog` class recording config, seed and per-step metrics, with `best(metric)` and `compare(a, b)` returning deltas.
- `12-03-study-winner` — `study_winner(runs, scientific_param, metric)` picking the best value of one parameter after taking the best over nuisance parameters, with ties broken by fewest steps.

## 13. Convolutional networks

**Learned when:** the Learner computes conv output shapes and parameter counts, and implements 2-D convolution plus max pooling by hand that matches an edge-detect kernel result.

**Teach:** convolution as cross-correlation (no flip); kernels, channels, padding, stride; output size `(n + 2p − k) / s + 1`; parameter sharing and translation equivariance; pooling; the receptive field growing with depth; feature maps; a LeNet-style stack conv → act → pool → linear.

**Probe:** thinking DL convolution flips the kernel; assuming one kernel per layer rather than in_channels × out_channels; counting pooling as learned; ignoring padding in the shape formula; forgetting the bias per output channel.

**Sources:** https://cs231n.stanford.edu/schedule.html (lec 5) · https://d2l.ai/ (ch 7)

**Exercises:**
- `13-01-conv-shapes-and-params` — `conv_output_size(n, k, p, s)` and `conv_params(in_c, out_c, k, bias)`.
- `13-02-conv2d-and-maxpool` — `conv2d(image, kernel, stride, padding)` and `maxpool2d(image, size, stride)` on a single channel, checked against hand results with an edge-detect kernel.
- `13-03-tiny-cnn-torch` — a small `nn.Module` CNN whose output shape on a 1×8×8 input is asserted layer by layer, and which fits a seeded synthetic bars-vs-stripes set in a few seconds.

## 14. Modern CNN ideas: residual connections and transfer learning

**Learned when:** the Learner explains why residual connections let deep nets train, and describes how to fine-tune a pretrained backbone on a small dataset (freeze, replace the head, discriminative LRs).

**Teach:** VGG blocks; the residual `x + F(x)` as a gradient highway; 1×1 conv for channel mixing; global average pooling; pretrained backbones; freezing vs fine-tuning; discriminative learning rates; fine-tuning as the default over training from scratch; residuals are everywhere in transformers (the handoff).

**Probe:** training from scratch by default; expecting a plain 50-layer net to train like a ResNet; freezing the new head instead of the backbone; assuming residual connections only matter for CNNs.

**Sources:** https://cs231n.stanford.edu/schedule.html (lec 6) · https://d2l.ai/ (ch 8) · https://course.fast.ai/ (lessons 1, 8)

**Exercises:**
- `14-01-residual-block` — `residual_block_forward(x, f)` on lists and a `ResidualMLP` block in PyTorch whose output equals `x + f(x)`.
- `14-02-gradient-highway` — a toy showing a product of many small derivatives vanishes while the `1 + d` residual form stays alive.
- `14-03-freeze-and-head` — `freeze_backbone(model)` and `replace_head(model, n_classes)` on a tiny `nn.Sequential`, leaving only the head's parameters trainable.

## 15. Vision tasks beyond classification: detection and segmentation

**Learned when:** the Learner explains what a detector outputs (boxes, classes, scores), what a segmenter outputs (a per-pixel class map), and how each is scored.

**Teach:** classification vs localization vs detection vs semantic and instance segmentation; bounding boxes and IoU; non-maximum suppression; anchor-based vs anchor-free detectors as a concept; mAP; segmentation as per-pixel classification with an encoder-decoder (U-Net) scored by per-class IoU; when a plain classifier is enough.

**Probe:** scoring a detector with plain accuracy; thinking segmentation needs a separate model per object; applying NMS across classes; confusing the IoU threshold for "correct" with the confidence threshold.

**Sources:** https://cs231n.stanford.edu/schedule.html (detection, segmentation) · https://www.deeplearning.ai/courses/deep-learning-specialization/ (course 4)

**Exercises:**
- `15-01-iou` — `iou(box_a, box_b)` for `[x1, y1, x2, y2]` boxes, zero for disjoint boxes.
- `15-02-non-max-suppression` — `nms(boxes, scores, iou_threshold)` returning kept indices in score order.
- `15-03-segmentation-iou` — `mean_iou(pred_mask, true_mask, n_classes)` per class and averaged, ignoring classes absent from both masks.

## 16. GPUs, performance and debugging training

**Learned when:** the Learner estimates a model's training memory, explains mixed precision and gradient accumulation, and works through the debugging checklist on a run that does not learn.

**Teach:** why GPUs (parallel matmul); `.to(device)` and host↔device transfer cost; batch size vs memory; float32, float16 and bfloat16; mixed precision with loss scaling; gradient accumulation; DataLoader workers; the checklist (overfit a tiny batch, check the initial loss, check the labels, check the LR, look at activations and gradients); seeds and reproducibility; free GPUs on Colab and Kaggle.

**Probe:** expecting a bigger GPU to fix a slow dataloader; fp16 without loss scaling silently underflowing; assuming `model.cuda()` moves the data too; believing the same seed makes GPU runs bit-identical.

**Sources:** https://d2l.ai/ (ch 6 GPUs, ch 13) · https://course.fast.ai/Lessons/part2.html (lesson 20) · https://cs231n.stanford.edu/schedule.html (lec 11)

**Exercises:**
- `16-01-training-memory` — `param_memory_mb(n_params, dtype)` and `adam_training_memory_mb(n_params)` (weights, grads, two moments).
- `16-02-grad-accum-schedule` — `grad_accum_schedule(micro_batches, accum)` returning the micro-batch indices at which `step()` runs, plus the loss scale factor.
- `16-03-simulate-fp16` — `to_fp16(x)` via `struct.pack('e')` reporting overflow to inf and underflow to zero, plus `loss_scale_ok(grads, scale)`.

## 17. Embeddings

**Learned when:** the Learner explains an embedding as a learned lookup table equal to one-hot × matrix, uses cosine similarity on it, and writes the scatter-add gradient for repeated indices.

**Teach:** one-hot → dense vector; the embedding matrix (vocab × dim); lookup equals matmul with a one-hot; learned by backprop like any weight; the word2vec idea of predicting context; embedding dimension; similarity search by cosine; embeddings for categorical features and collaborative filtering.

**Probe:** thinking embeddings are hand-designed; reading meaning into single dimensions; taking king − man + woman as typical rather than cherry-picked; forgetting that a repeated index accumulates gradient.

**Sources:** https://developers.google.com/machine-learning/crash-course (Embeddings) · https://d2l.ai/ (ch 15) · https://karpathy.ai/zero-to-hero.html (makemore part 2)

**Exercises:**
- `17-01-embed-equals-onehot` — `embed(indices, table)` with a test that it equals `one_hot(indices) @ table`.
- `17-02-most-similar` — `most_similar(word, table, vocab, k)` by cosine, excluding the query word.
- `17-03-embedding-grad` — `embedding_grad(indices, dout, vocab_size, dim)` scatter-adding, with a repeated index summing its contributions.

## 18. Sequence modeling: n-gram LM → MLP LM → RNN, LSTM, GRU

**Learned when:** the Learner builds a character-level bigram model from counts and samples from it, evaluates NLL, implements RNN and LSTM cell forwards, and explains why attention replaced recurrence.

**Teach:** language modeling = next-token prediction; bigram counts with smoothing; sampling with temperature; NLL and perplexity; a fixed-context-window MLP LM (Bengio 2003); the RNN hidden state and weight sharing across time; backprop through time; vanishing and exploding gradients over long sequences; LSTM and GRU gates; teacher forcing; recurrence is sequential and forgets, attention looks at everything at once (the handoff to Phase 10).

**Probe:** thinking RNNs remember everything; comparing perplexities across different tokenizers; conflating greedy decoding with sampling; believing the LSTM cell state and hidden state are the same thing; forgetting that the same weights are used at every timestep.

**Sources:** https://karpathy.ai/zero-to-hero.html (makemore parts 1–2, 5) · https://d2l.ai/ (ch 9–10) · https://cs231n.stanford.edu/schedule.html (lec 7)

**Exercises:**
- `18-01-bigram-lm` — `bigram_counts(words)`, `bigram_probs(counts, smoothing)`, seeded `sample(probs, rng, n)` and `avg_nll(words, probs)`.
- `18-02-rnn-forward` — `rnn_forward(xs, h0, Wxh, Whh, b)` over a short sequence with lists, matching a hand trace.
- `18-03-lstm-cell` — `lstm_cell(x, h, c, params)` returning the new (h, c), checked against `torch.nn.LSTMCell` with the same weights.

## 19. Capstone: a tiny CNN and a character-level LM from scratch

**Learned when:** the Learner trains, in PyTorch with their own loop, a small CNN on synthetic images and a character-level MLP LM on a tiny corpus, and writes up loss curves and an ablation (init, normalization, dropout, optimizer) using the run log from Topic 12.

**Teach:** composing everything: data → model → loss → optimizer → schedule → eval; the ablation habit (change one thing, keep the seed); reading a loss curve; what the char LM's samples show as the loss falls; where this stops (fixed context, no attention) and why Phase 10 starts with tokenization and attention.

**Probe:** comparing ablations run with different seeds; reporting training loss as the result; running the ablation on the test split; claiming the char LM "understands" words.

**Sources:** https://karpathy.ai/zero-to-hero.html (makemore part 2) · https://github.com/karpathy/micrograd · https://d2l.ai/ (ch 7–9)

**Exercises:**
- `19-01-char-mlp-lm` — a Bengio-style `CharMLP(vocab, block, dim, hidden)` in PyTorch plus `make_dataset(words, block)`, trained on a seeded tiny word list until the NLL falls below a threshold.
- `19-02-ablation-table` — `ablation_table(runs, baseline)` producing per-run metric deltas vs the baseline and flagging runs whose seed differs.
- `19-03-train-eval-loop` — `train_and_eval(model, train, val, epochs, make_optimizer)` returning per-epoch train/val losses with the val loss computed under `no_grad` in eval mode, tested on a tiny CNN over seeded synthetic images.
