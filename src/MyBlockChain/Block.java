package MyBlockChain;

import java.util.Date;

public class Block {

    public String hash;
    public String previousHash;

    private String data;
    private long timeStamp;
    private int nonce;

    public Block(String data, String previousHash) {
        this.data = data;
        this.previousHash = previousHash;
        this.timeStamp = new Date().getTime();
        this.hash = calculateHash();
    }

    public String calculateHash() {
        return StringUtil.applySha256(previousHash
                + Long.toString(timeStamp)
                + Integer.toString(nonce)
                + data);
    }

    /*
        Simulated the mining of a block
        Try different value for the nonce until the hash has the required number of zero
     */
    public void mineBlock(int difficulty) {
        String target = new String(new char[difficulty]).replace('\0', '0');
        while(!hash.substring(0, difficulty).equals(target)) {
            nonce++;
            hash = calculateHash();
        }
        System.out.println("Block Mined!! : " + hash);
    }
}
