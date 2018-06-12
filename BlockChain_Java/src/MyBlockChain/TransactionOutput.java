package MyBlockChain;

import java.security.PublicKey;

/*
    Transaction outputs will show the final amount sent to each party
    from the transaction. Act as proof that you have coins to send.
 */
public class TransactionOutput {
    public String id;
    public PublicKey reciepient; // owner of these coins
    public float value;
    public String parentTransactionId; // the id of the transaction this ouput was created in

    public TransactionOutput(PublicKey reciepient, float value, String parentTransactionId) {
        this.reciepient = reciepient;
        this.value = value;
        this.parentTransactionId = parentTransactionId;
        this.id = StringUtil.applySha256(StringUtil.getStringFromKey(reciepient)
                + Float.toString(value)
                + parentTransactionId);
    }

    public boolean isMine(PublicKey publicKey) {
        return (publicKey == reciepient);
    }
}
