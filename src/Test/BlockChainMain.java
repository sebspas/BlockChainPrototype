package Test;


import MyBlockChain.*;

import java.security.Security;

public class BlockChainMain {

    public static Wallet walletA;
    public static Wallet walletB;

    public static void main(String[] args) {

        //Setup Bouncey castle as a Security Provider
        Security.addProvider(new org.bouncycastle.jce.provider.BouncyCastleProvider());
        //Create the new wallets
        walletA = new Wallet();
        walletB = new Wallet();

        //Test public and private keys
        System.out.println("Private and public keys:");
        System.out.println(StringUtil.getStringFromKey(walletA.privateKey));
        System.out.println(StringUtil.getStringFromKey(walletA.publicKey));
        //Create a test transaction from WalletA to walletB
        Transaction transaction = new Transaction(walletA.publicKey, walletB.publicKey, 5, null);
        transaction.generateSignature(walletA.privateKey);
        //Verify the signature works and verify it from the public key
        System.out.println("Is signature verified");
        System.out.println(transaction.verifiySignature());

        BlockChain blockChain = BlockChain.getInstance();

        blockChain.addBlock(new Block("Origin block", "0"));
        System.out.println("Trying to Mine block 1... ");
        blockChain.get(0).mineBlock(BlockChain.difficulty);

        blockChain.addBlock(new Block("Second block", blockChain.getLastBlock().hash));
        System.out.println("Trying to Mine block 2... ");
        blockChain.get(1).mineBlock(BlockChain.difficulty);

        blockChain.addBlock(new Block("Third block", blockChain.getLastBlock().hash));
        System.out.println("Trying to Mine block 3... ");
        blockChain.get(2).mineBlock(BlockChain.difficulty);

        System.out.println("\nBlockchain is Valid: " + blockChain.isChainValid());

        System.out.println("\nThe block chain: ");
        System.out.println(blockChain.getJSON());
    }
}
