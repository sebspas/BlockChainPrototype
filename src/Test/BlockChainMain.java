package Test;

import BlockChain.Block;
import BlockChain.BlockChain;

public class BlockChainMain {

    public static void main(String[] args) {
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
