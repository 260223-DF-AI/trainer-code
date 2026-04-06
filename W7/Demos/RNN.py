import torch
import torch.nn as nn
from torch.nn.utils.rnn import pad_sequence

class TextClassifier(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim, num_classes):
        super(TextClassifier, self).__init__()

        self.embedding = nn.Embedding(num_embeddings=vocab_size,
                                      embedding_dim=embedding_dim,
                                      padding_idx=0) # the padding 0 = <PAD> 
        self.lstm = nn.LSTM(input_size=embedding_dim, # the embedding dimension, coming out of the Embedding
                            hidden_size=hidden_dim, # the size of the memory vector
                            batch_first=True) # the batch dimension comes first

        self.fc = nn.Linear(hidden_dim, num_classes)

    def forward(self, x):
        embedded = self.embedding(x)
        out, (hn, cn) = self.lstm(embedded)
        print( out.shape )
        print( hn.shape )
        print( cn.shape )
        return self.fc(hn[0])
    
def lstm_run():
    # I love pytorch - 3
    # [ 1, 2, 3]
    # I hate bugs    - 3
    # [ 1, 4, 5]
    # pytorch <PAD> <PAD> - 3
    # [3, 0, 0]

#    0   1   2   3       4    5
#  <PAD> I love pytorch hate bugs

    vocab_size = 6
    seq1 = torch.tensor([1, 2, 3])
    seq2 = torch.tensor([1, 4, 5])
    seq3 = torch.tensor([3])
    sequences = [seq1, seq2, seq3]
    lengths = torch.tensor([len(seq) for seq in sequences])

    padded_batch = pad_sequence(sequences, batch_first=True, padding_value=0)
    
    # print( padded_batch.shape )
    # print( lengths.shape )

    embedding_dim = 16 # the embedding dimension: 16-number vector
    hidden_dim = 32 # the memory occupied by the hidden state vector: 32-number vector
    num_classes = 2 # negative/positive sentiment

    model = TextClassifier(vocab_size, embedding_dim, hidden_dim, num_classes)

    pred = model(padded_batch)

    print( f"Prediciton shape: {pred.shape}")



def main():
    lstm_run()

if __name__ == "__main__":
    main()