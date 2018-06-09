package MyBlockChain;

/*
    Class will be used to reference transactionOutputs that have
    not yet been spent
 */
public class TransactionInput {
    public String transactionOutputId; // reference to transactionOutputs -> transactionId
    public TransactionOutput UTXO; // Contains the unspent transaction output

    public TransactionInput(String transactionOutputId) {
        this.transactionOutputId = transactionOutputId;
    }
}
