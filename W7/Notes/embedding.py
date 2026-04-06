import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt

# =============================================================================
# Change this text to see how the embeddings adapt!
# The model will learn which words appear in similar contexts.
# Try substituting words, or adding new sentences.
# =============================================================================
TEXT = """
a king is a regal man .
a queen is a regal woman .
a boy is a young man .
a girl is a young woman .
a prince is a young king .
a princess is a young queen .
a prince is a regal boy .
a princess is a regal girl .
"""

# --- 1. Data Preparation ---
# Tokenize and build vocabulary
words = TEXT.lower().split()
vocab = list(set(words))
word_to_ix = {w: i for i, w in enumerate(vocab)}

# Generate context-target pairs (CBOW: predict center word from context)
# We use a window of 1 word before and 1 word after
CONTEXT_SIZE = 1
data = []
for i in range(CONTEXT_SIZE, len(words) - CONTEXT_SIZE):
    context = [words[i - 1], words[i + 1]]
    target = words[i]
    data.append((context, target))

# --- 2. Model Definition ---
class CBOW(nn.Module):
    def __init__(self, vocab_size, embedding_dim):
        super(CBOW, self).__init__()
        # The embedding layer maps integer indices to dense vectors
        self.embeddings = nn.Embedding(vocab_size, embedding_dim)
        self.linear = nn.Linear(embedding_dim, vocab_size)

    def forward(self, inputs):
        # Get embeddings for context words and average them
        embeds = self.embeddings(inputs).mean(dim=0).unsqueeze(0)
        # Predict the probability of each word in the vocabulary being the target
        out = self.linear(embeds)
        return out

# --- 3. Training Loop ---
# We use 2 dimensions so we can graph them directly!
EMBEDDING_DIM = 2 
model = CBOW(len(vocab), EMBEDDING_DIM)
loss_function = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.03)

print("Training embedding model on the text...")
for epoch in range(150):
    total_loss = 0
    for context, target in data:
        # Prepare inputs and targets as PyTorch tensors
        context_idxs = torch.tensor([word_to_ix[w] for w in context], dtype=torch.long)
        target_idx = torch.tensor([word_to_ix[target]], dtype=torch.long)

        model.zero_grad()
        log_probs = model(context_idxs)
        loss = loss_function(log_probs, target_idx)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
        
    if (epoch + 1) % 30 == 0:
         print(f"Epoch {epoch+1:3d} | Loss: {total_loss:.4f}")

# --- 4. Visualizing the Embeddings ---
# Extract the learned embedding matrix
trained_embeddings = model.embeddings.weight.data.clone()

plt.figure(figsize=(10, 8))
# Plot each word's embedding
for word, i in word_to_ix.items():
    x, y = trained_embeddings[i].numpy()
    plt.scatter(x, y, color='blue')
    plt.annotate(word, (x, y), xytext=(5, 2), textcoords='offset points')

plt.title("Learned Word Embeddings (2D Space)")
plt.xlabel("Embedding Dimension 1")
plt.ylabel("Embedding Dimension 2")
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()