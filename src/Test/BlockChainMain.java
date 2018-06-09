package Test;

import BlockChain.Block;

public class BlockChainMain {

    public static void main(String[] args) {
        Block genesisBlock = new Block("Origin block", "0");
        System.out.println("Hash for block 1 : " + genesisBlock.hash);

        Block secondBlock = new Block("Second block", genesisBlock.hash);
        System.out.println("Hash for block 2 : " + secondBlock.hash);

        Block thirdBlock = new Block("Third block", secondBlock.hash);
        System.out.println("Hash for block 3 : " + thirdBlock.hash);
    }
}
